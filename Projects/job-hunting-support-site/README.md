# Job Hunting Support Site Prototype

Static prototype for the `.company` project `job-hunting-support-site`.

## Run

```bash
node -e "const http=require('http'),fs=require('fs'),path=require('path');const root=process.cwd();http.createServer((req,res)=>{const u=new URL(req.url,'http://127.0.0.1');let f=path.join(root,u.pathname==='/'?'index.html':u.pathname);fs.readFile(f,(e,d)=>{if(e){res.writeHead(404);return res.end('not found')}res.writeHead(200,{'content-type':f.endsWith('.html')?'text/html; charset=utf-8':'text/plain; charset=utf-8'});res.end(d)})}).listen(4173,'127.0.0.1',()=>console.log('http://127.0.0.1:4173/'))"
```

Open `http://localhost:4173/`.
