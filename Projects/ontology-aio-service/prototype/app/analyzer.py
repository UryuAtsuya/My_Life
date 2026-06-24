from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from html import unescape
from typing import Any
from urllib.parse import urljoin, urlparse, urlunparse
from xml.etree import ElementTree

import requests
from bs4 import BeautifulSoup


REQUEST_TIMEOUT_SECONDS = 10
MAX_SITEMAP_URLS = 20
MAX_FALLBACK_LINKS = 10
MAX_TOTAL_PAGES = 29
USER_AGENT = "OntologyAIOPrototype/0.1 (+local diagnostic tool)"


class AnalysisError(Exception):
    """Raised when a URL cannot be analyzed."""


@dataclass
class PageAnalysis:
    url: str
    status_code: int | None = None
    title: str = ""
    meta_description: str = ""
    canonical: str = ""
    h1: list[str] = field(default_factory=list)
    h2: list[str] = field(default_factory=list)
    internal_links: list[str] = field(default_factory=list)
    schema_types: list[str] = field(default_factory=list)
    has_json_ld: bool = False
    has_microdata: bool = False
    faq_signals: list[str] = field(default_factory=list)
    text_excerpt: str = ""
    error: str = ""


@dataclass
class CheckItem:
    label: str
    status: str
    detail: str
    recommendation: str


@dataclass
class ScoreCard:
    name: str
    score: int
    rationale: str


@dataclass
class BacklogItem:
    priority: str
    title: str
    reason: str
    output: str


@dataclass
class AnalysisResult:
    input_url: str
    normalized_url: str
    pages: list[PageAnalysis]
    source: str
    sitemap_url: str | None
    scores: list[ScoreCard]
    overall_score: int
    checks: list[CheckItem]
    seo_to_ontology: list[dict[str, str]]
    backlog: list[BacklogItem]
    warnings: list[str]


def analyze_site(raw_url: str) -> AnalysisResult:
    normalized_url = normalize_url(raw_url)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    homepage = fetch_and_parse(session, normalized_url)
    if homepage.error:
        raise AnalysisError(homepage.error)

    sitemap_url = root_url(normalized_url) + "/sitemap.xml"
    candidate_urls, sitemap_warnings = discover_sitemap_urls(
        session=session,
        sitemap_url=sitemap_url,
        domain=domain_of(normalized_url),
    )
    source = "sitemap.xml"

    if not candidate_urls:
        candidate_urls = homepage.internal_links[:MAX_FALLBACK_LINKS]
        source = "internal links"

    urls = unique_urls([normalized_url, *candidate_urls])[:MAX_TOTAL_PAGES]
    pages = [homepage]
    for url in urls[1:]:
        pages.append(fetch_and_parse(session, url))

    scores = build_scores(pages, source)
    checks = build_checks(pages, source)
    overall_score = round(sum(score.score for score in scores) / len(scores))

    return AnalysisResult(
        input_url=raw_url,
        normalized_url=normalized_url,
        pages=pages,
        source=source,
        sitemap_url=sitemap_url if source == "sitemap.xml" else None,
        scores=scores,
        overall_score=overall_score,
        checks=checks,
        seo_to_ontology=build_ontology_rows(pages),
        backlog=build_backlog(checks),
        warnings=sitemap_warnings,
    )


def normalize_url(raw_url: str) -> str:
    value = raw_url.strip()
    if not value:
        raise AnalysisError("URLを入力してください。")
    if "://" not in value:
        value = f"https://{value}"

    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        raise AnalysisError("http または https のURLだけを指定できます。")
    if not parsed.netloc or "." not in parsed.netloc:
        raise AnalysisError("有効なドメインを含むURLを指定してください。")

    path = parsed.path or "/"
    return urlunparse((parsed.scheme, parsed.netloc.lower(), path, "", parsed.query, ""))


def fetch_and_parse(session: requests.Session, url: str) -> PageAnalysis:
    page = PageAnalysis(url=url)
    try:
        response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS, allow_redirects=True)
        page.status_code = response.status_code
        response.raise_for_status()
    except requests.RequestException as exc:
        page.error = f"{url} の取得に失敗しました: {exc}"
        return page

    content_type = response.headers.get("content-type", "")
    if "html" not in content_type and not response.text.lstrip().startswith("<"):
        page.error = f"{url} はHTMLとして解析できませんでした。"
        return page

    soup = BeautifulSoup(response.text, "html.parser")
    page.title = clean_text(soup.title.string if soup.title else "")
    page.meta_description = meta_content(soup, "description")
    page.canonical = canonical_href(soup, response.url)
    page.h1 = [clean_text(node.get_text(" ")) for node in soup.find_all("h1") if clean_text(node.get_text(" "))]
    page.h2 = [clean_text(node.get_text(" ")) for node in soup.find_all("h2") if clean_text(node.get_text(" "))]
    page.internal_links = extract_internal_links(soup, response.url)
    page.schema_types, page.has_json_ld = extract_schema_types(soup)
    page.has_microdata = bool(soup.find(attrs={"itemscope": True}) or soup.find(attrs={"itemtype": True}))
    page.faq_signals = extract_faq_signals(soup, page.schema_types)
    page.text_excerpt = clean_text(soup.get_text(" "))[:1200]
    page.url = response.url
    return page


def discover_sitemap_urls(
    session: requests.Session,
    sitemap_url: str,
    domain: str,
) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    try:
        response = session.get(sitemap_url, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException:
        return [], [f"{sitemap_url} を取得できなかったため、内部リンク解析にフォールバックしました。"]

    urls = parse_sitemap(response.text, domain)
    child_sitemaps = [url for url in urls if url.endswith(".xml")][:3]
    page_urls = [url for url in urls if not url.endswith(".xml")]

    for child_url in child_sitemaps:
        if len(page_urls) >= MAX_SITEMAP_URLS:
            break
        try:
            child_response = session.get(child_url, timeout=REQUEST_TIMEOUT_SECONDS)
            child_response.raise_for_status()
        except requests.RequestException:
            warnings.append(f"{child_url} の取得に失敗しました。")
            continue
        page_urls.extend(url for url in parse_sitemap(child_response.text, domain) if not url.endswith(".xml"))

    return unique_urls(page_urls)[:MAX_SITEMAP_URLS], warnings


def parse_sitemap(xml_text: str, domain: str) -> list[str]:
    urls: list[str] = []
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError:
        return urls

    for loc in root.iter():
        if not loc.tag.endswith("loc") or not loc.text:
            continue
        value = clean_text(loc.text)
        if value and domain_of(value) == domain:
            urls.append(value)
    return urls


def build_scores(pages: list[PageAnalysis], source: str) -> list[ScoreCard]:
    successful_pages = [page for page in pages if not page.error]
    schema_types = all_schema_types(successful_pages)
    text = corpus_text(successful_pages)
    link_urls = " ".join(link for page in successful_pages for link in page.internal_links).lower()

    seo_points = [
        any(page.status_code and 200 <= page.status_code < 300 for page in successful_pages),
        bool(successful_pages and successful_pages[0].title),
        bool(successful_pages and successful_pages[0].meta_description),
        bool(successful_pages and successful_pages[0].h1),
        bool(successful_pages and successful_pages[0].canonical),
        source == "sitemap.xml",
        len(successful_pages) > 1,
        any(page.internal_links for page in successful_pages),
    ]
    seo_score = percent(seo_points)

    entity_points = [
        has_any_schema(schema_types, {"Organization", "LocalBusiness"}),
        has_any_schema(schema_types, {"Service", "Product"}),
        contains_any(text, CATEGORY_TERMS),
        contains_any(text, AUDIENCE_TERMS),
        contains_any(text, PROBLEM_TERMS),
        contains_any(text, COMPARISON_TERMS),
        contains_any(text, EVIDENCE_TERMS),
    ]
    entity_score = percent(entity_points)

    structured_points = [
        any(page.has_json_ld for page in successful_pages),
        bool(schema_types),
        has_any_schema(schema_types, {"Organization", "LocalBusiness"}),
        has_any_schema(schema_types, {"Service", "Product"}),
        has_any_schema(schema_types, {"FAQPage"}),
        has_any_schema(schema_types, {"BreadcrumbList"}),
        has_any_schema(schema_types, {"Article", "BlogPosting", "NewsArticle"}),
        has_any_schema(schema_types, {"Review", "AggregateRating"}),
    ]
    structured_score = percent(structured_points)

    graph_points = [
        contains_any(link_urls + text, FAQ_TERMS),
        contains_any(link_urls + text, COMPARISON_TERMS),
        contains_any(link_urls + text, PRICING_TERMS),
        contains_any(link_urls + text, CASE_STUDY_TERMS),
        contains_any(link_urls + text, GLOSSARY_TERMS),
        contains_any(link_urls + text, ABOUT_TERMS),
        len(successful_pages) >= 3,
    ]
    graph_score = percent(graph_points)

    aio_score = round(
        seo_score * 0.25
        + entity_score * 0.30
        + structured_score * 0.25
        + graph_score * 0.20
    )

    return [
        ScoreCard("AIO Readiness Score", aio_score, "SEO基盤、Entity明確性、構造化データ、Content Graphの加重平均です。"),
        ScoreCard("SEO Foundation Score", seo_score, "title/meta/h1/canonical/sitemap/internal links/statusの充足度です。"),
        ScoreCard("Entity / Ontology Score", entity_score, "Organization、Service/Product、カテゴリ、対象顧客、課題、比較、証拠情報の明確さです。"),
        ScoreCard("Structured Data Score", structured_score, "JSON-LDと主要schema.org typeの実装状況です。"),
        ScoreCard("Content Graph Score", graph_score, "FAQ、比較、料金、事例、用語、会社情報への接続状況です。"),
    ]


def build_checks(pages: list[PageAnalysis], source: str) -> list[CheckItem]:
    successful_pages = [page for page in pages if not page.error]
    homepage = successful_pages[0] if successful_pages else PageAnalysis(url="")
    schema_types = all_schema_types(successful_pages)
    text = corpus_text(successful_pages)
    link_urls = " ".join(link for page in successful_pages for link in page.internal_links).lower()

    return [
        check("HTTP 200", bool(homepage.status_code and 200 <= homepage.status_code < 300), "トップページが正常に取得できる", "取得エラーやリダイレクトを確認する"),
        check("title", bool(homepage.title), homepage.title or "titleが未検出", "サービス名、カテゴリ、主要価値を含める"),
        check("meta description", bool(homepage.meta_description), homepage.meta_description or "meta descriptionが未検出", "AI回答に使いやすい公式説明を入れる"),
        check("h1", bool(homepage.h1), ", ".join(homepage.h1[:2]) or "h1が未検出", "ページ主題を1つ明確にする"),
        check("canonical", bool(homepage.canonical), homepage.canonical or "canonicalが未検出", "正規URLを明示する"),
        check("sitemap.xml", source == "sitemap.xml", "sitemapからページ候補を取得" if source == "sitemap.xml" else "sitemap未検出", "sitemap.xmlを公開して主要ページを含める"),
        check("Organization schema", has_any_schema(schema_types, {"Organization", "LocalBusiness"}), schema_detail(schema_types), "Organization / LocalBusinessをJSON-LDで明示する"),
        check("Service / Product schema", has_any_schema(schema_types, {"Service", "Product"}), schema_detail(schema_types), "サービスまたは商品をschema.orgで表現する"),
        check("FAQ", has_any_schema(schema_types, {"FAQPage"}) or contains_any(link_urls + text, FAQ_TERMS), "FAQPageまたはFAQらしい情報を検出", "導入前の質問をFAQPageとして整理する"),
        check("比較情報", contains_any(link_urls + text, COMPARISON_TERMS), "比較・競合差分の手がかりを検出", "競合との差分や選定基準ページを作る"),
        check("料金情報", contains_any(link_urls + text, PRICING_TERMS), "料金・プランの手がかりを検出", "料金/プラン/見積もり条件を明確にする"),
        check("証拠情報", contains_any(link_urls + text, CASE_STUDY_TERMS + EVIDENCE_TERMS), "事例・実績・レビューの手がかりを検出", "導入事例、実績、レビュー、監修者情報を増やす"),
    ]


def build_ontology_rows(pages: list[PageAnalysis]) -> list[dict[str, str]]:
    homepage = next((page for page in pages if not page.error), PageAnalysis(url=""))
    schema_types = all_schema_types([page for page in pages if not page.error])
    return [
        {
            "seo": "title",
            "current": homepage.title or "未検出",
            "entity": "Service / Product / Category",
            "schema": "WebPage, Service, Product",
            "action": "カテゴリ名と提供価値が分かるtitleにする",
        },
        {
            "seo": "meta description",
            "current": homepage.meta_description or "未検出",
            "entity": "公式説明 / 対象顧客 / 提供価値",
            "schema": "WebPage, Service",
            "action": "LLMが引用しやすい1-2文の公式説明にする",
        },
        {
            "seo": "h1 / h2",
            "current": ", ".join([*homepage.h1[:1], *homepage.h2[:3]]) or "未検出",
            "entity": "Category / Problem / Feature / Audience",
            "schema": "Article, FAQPage, Service",
            "action": "課題、対象顧客、機能、比較軸を見出しで分ける",
        },
        {
            "seo": "JSON-LD / microdata",
            "current": schema_detail(schema_types),
            "entity": "Organization / Service / Product / FAQ",
            "schema": "Organization, Service, Product, FAQPage",
            "action": "ページ上の事実と一致するschema.orgを追加する",
        },
        {
            "seo": "internal links",
            "current": f"{len(homepage.internal_links)} links detected",
            "entity": "Entity relationship",
            "schema": "BreadcrumbList, WebPage",
            "action": "FAQ、料金、事例、比較、用語ページへ接続する",
        },
    ]


def build_backlog(checks: list[CheckItem]) -> list[BacklogItem]:
    backlog: list[BacklogItem] = []
    priority_order = {"Missing": "P0", "Weak": "P1", "OK": "P2"}
    for item in checks:
        if item.status == "OK":
            continue
        backlog.append(
            BacklogItem(
                priority=priority_order[item.status],
                title=item.label,
                reason=item.detail,
                output=item.recommendation,
            )
        )
    return backlog[:8]


def check(label: str, passed: bool, detail: str, recommendation: str) -> CheckItem:
    status = "OK" if passed else "Missing"
    if passed and not detail:
        status = "Weak"
    return CheckItem(label, status, detail, recommendation)


def extract_schema_types(soup: BeautifulSoup) -> tuple[list[str], bool]:
    schema_types: list[str] = []
    has_json_ld = False
    for script in soup.find_all("script", attrs={"type": re.compile("ld\\+json", re.I)}):
        if not script.string:
            continue
        has_json_ld = True
        try:
            payload = json.loads(script.string)
        except json.JSONDecodeError:
            continue
        schema_types.extend(flatten_schema_types(payload))

    for node in soup.find_all(attrs={"itemtype": True}):
        itemtype = node.get("itemtype", "")
        if "schema.org/" in itemtype:
            schema_types.append(itemtype.rstrip("/").split("/")[-1])

    return sorted(set(schema_types)), has_json_ld


def flatten_schema_types(payload: Any) -> list[str]:
    found: list[str] = []
    if isinstance(payload, dict):
        schema_type = payload.get("@type")
        if isinstance(schema_type, str):
            found.append(schema_type)
        elif isinstance(schema_type, list):
            found.extend(str(value) for value in schema_type)
        for value in payload.values():
            found.extend(flatten_schema_types(value))
    elif isinstance(payload, list):
        for item in payload:
            found.extend(flatten_schema_types(item))
    return found


def extract_internal_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    base_domain = domain_of(base_url)
    links: list[str] = []
    for node in soup.find_all("a", href=True):
        href = node["href"].strip()
        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absolute = urljoin(base_url, href)
        parsed = urlparse(absolute)
        cleaned = urlunparse((parsed.scheme, parsed.netloc.lower(), parsed.path or "/", "", parsed.query, ""))
        if parsed.scheme in {"http", "https"} and domain_of(cleaned) == base_domain:
            links.append(cleaned)
    return unique_urls(links)


def extract_faq_signals(soup: BeautifulSoup, schema_types: list[str]) -> list[str]:
    signals = ["FAQPage schema"] if "FAQPage" in schema_types else []
    for heading in soup.find_all(["h1", "h2", "h3"]):
        text = clean_text(heading.get_text(" "))
        if contains_any(text.lower(), FAQ_TERMS):
            signals.append(text)
    return unique_strings(signals)


def meta_content(soup: BeautifulSoup, name: str) -> str:
    node = soup.find("meta", attrs={"name": re.compile(f"^{name}$", re.I)})
    if not node:
        node = soup.find("meta", attrs={"property": re.compile(f"^og:{name}$", re.I)})
    return clean_text(node.get("content", "")) if node else ""


def canonical_href(soup: BeautifulSoup, base_url: str) -> str:
    node = soup.find("link", attrs={"rel": lambda value: value and "canonical" in value})
    return urljoin(base_url, node.get("href", "")) if node else ""


def root_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def domain_of(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.")


def unique_urls(urls: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        unique.append(url)
    return unique


def unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", unescape(value)).strip()


def all_schema_types(pages: list[PageAnalysis]) -> set[str]:
    return {schema_type for page in pages for schema_type in page.schema_types}


def corpus_text(pages: list[PageAnalysis]) -> str:
    parts: list[str] = []
    for page in pages:
        parts.extend([page.title, page.meta_description, " ".join(page.h1), " ".join(page.h2), page.text_excerpt])
    return " ".join(parts).lower()


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def has_any_schema(schema_types: set[str], targets: set[str]) -> bool:
    return bool(schema_types.intersection(targets))


def schema_detail(schema_types: set[str]) -> str:
    return ", ".join(sorted(schema_types)) if schema_types else "schema.org type未検出"


def percent(points: list[bool]) -> int:
    if not points:
        return 0
    return round(sum(1 for point in points if point) / len(points) * 100)


CATEGORY_TERMS = (
    "サービス",
    "ソリューション",
    "カテゴリ",
    "業界",
    "ツール",
    "platform",
    "service",
    "solution",
    "software",
    "tool",
)
AUDIENCE_TERMS = (
    "法人",
    "企業",
    "中小企業",
    "担当者",
    "マーケティング",
    "経営者",
    "for ",
    "teams",
    "business",
)
PROBLEM_TERMS = (
    "課題",
    "問題",
    "解決",
    "改善",
    "効率化",
    "problem",
    "solve",
    "improve",
    "optimize",
)
COMPARISON_TERMS = (
    "比較",
    "競合",
    "違い",
    "選び方",
    "代替",
    "compare",
    "comparison",
    "alternative",
    "vs",
)
EVIDENCE_TERMS = (
    "事例",
    "実績",
    "レビュー",
    "導入",
    "お客様",
    "case study",
    "review",
    "testimonial",
    "customer",
)
FAQ_TERMS = ("faq", "q&a", "よくある質問", "質問", "ヘルプ")
PRICING_TERMS = ("料金", "価格", "プラン", "費用", "pricing", "price", "plan")
CASE_STUDY_TERMS = ("事例", "導入事例", "実績", "case", "customer", "story")
GLOSSARY_TERMS = ("用語", "辞典", "glossary", "dictionary", "terms")
ABOUT_TERMS = ("会社", "about", "company", "team", "代表", "監修")
