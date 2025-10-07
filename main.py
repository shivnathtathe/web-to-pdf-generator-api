# import re
# import json
# from pathlib import Path
# from fastapi import FastAPI, Query, HTTPException
# from fastapi.responses import FileResponse
# from playwright.async_api import async_playwright
# from fastapi.middleware.cors import CORSMiddleware
# import asyncio
# import sys

# # if sys.platform == "win32":
# #     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 	
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load config.json
# CONFIG_PATH = Path(__file__).parent / "config.json"
# default_config = {
#     "default": {
#         "A4": {"margin": {"top": "30px", "right": "0px", "bottom": "30px", "left": "0px"}},
#         "A5": {"margin": {"top": "5mm", "right": "0mm", "bottom": "5mm", "left": "0mm"}}
#     }
# }
# try:
#     if CONFIG_PATH.exists():
#         with open(CONFIG_PATH, "r", encoding="utf-8") as f:
#             content = f.read().strip()
#             if content:  # file is not empty
#                 PDF_CONFIG = json.loads(content)
#             else:
#                 print("⚠️ config.json is empty, using default config")
#                 PDF_CONFIG = default_config
#     else:
#         print("⚠️ config.json not found, using default config")
#         PDF_CONFIG = default_config
# except Exception as e:
#     print(f"⚠️ Error loading config.json: {e}. Falling back to default config.")
#     PDF_CONFIG = default_config


# async def generate_pdf(format_: str, url: str, output: str, tenant: str):
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()
#         await page.goto(url, wait_until="networkidle")
#         await page.wait_for_timeout(2000)
#         await page.evaluate("() => document.fonts.ready")

#         await page.add_style_tag(content="""
#             html, body {
#                 margin: 0 !important;
#                 padding: 0 !important;
#             }
#             .pagebreakbefore {
#                 break-before: page;
#                 page-break-before: always;
#             }
#         """)

#         # Get tenant-specific config, fallback to default
#         tenant_config = PDF_CONFIG.get(tenant, PDF_CONFIG["default"])
#         config = tenant_config.get(format_, tenant_config.get("A4"))

#         if not config:
#             raise HTTPException(status_code=400, detail=f"No config found for {format_}")

#         await page.pdf(
#             path=output,
#             format=format_,
#             print_background=True,
#             margin=config["margin"],
#             prefer_css_page_size=True
#         )

#         await browser.close()
#         return output


# @app.get("/generate-pdf")
# async def generate_pdf_api(
#     url: str = Query(..., description="URL of the HTML page"),
#     tenant: str = Query("default", description="Tenant name (multi-tenant configs)")
# ):
#     """
#     Converts a given HTML page to PDF.
#     Auto-detects format from URL like '::A4' or '::A5'.
#     Uses config.json for margins (multi-tenant).
#     """
#     match = re.search(r"::(A\d+)", url)
#     if not match:
#         raise HTTPException(status_code=400, detail="Format (A4, A5, etc.) not found in URL")

#     format_ = match.group(1)

#     output_filename = f"{tenant}_{format_}.pdf"

#     pdf_path = await generate_pdf(format_, url, output_filename, tenant)

#     return FileResponse(pdf_path, filename=output_filename, media_type="application/pdf")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

#Timeout
# import re
# import json
# from pathlib import Path
# from fastapi import FastAPI, Query, HTTPException
# from fastapi.responses import FileResponse
# from playwright.sync_api import sync_playwright
# from fastapi.middleware.cors import CORSMiddleware
# import asyncio
# from concurrent.futures import ThreadPoolExecutor

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load config.json
# CONFIG_PATH = Path(__file__).parent / "config.json"
# default_config = {
#     "default": {
#         "A4": {"margin": {"top": "30px", "right": "0px", "bottom": "30px", "left": "0px"}},
#         "A5": {"margin": {"top": "5mm", "right": "0mm", "bottom": "5mm", "left": "0mm"}}
#     }
# }
# try:
#     if CONFIG_PATH.exists():
#         with open(CONFIG_PATH, "r", encoding="utf-8") as f:
#             content = f.read().strip()
#             if content:
#                 PDF_CONFIG = json.loads(content)
#             else:
#                 print("⚠️ config.json is empty, using default config")
#                 PDF_CONFIG = default_config
#     else:
#         print("⚠️ config.json not found, using default config")
#         PDF_CONFIG = default_config
# except Exception as e:
#     print(f"⚠️ Error loading config.json: {e}. Falling back to default config.")
#     PDF_CONFIG = default_config


# # Thread pool for running sync playwright
# executor = ThreadPoolExecutor(max_workers=3)


# def generate_pdf_sync(format_: str, url: str, output: str, tenant: str):
#     """Synchronous version of generate_pdf using sync_playwright"""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url, wait_until="networkidle")
#         page.wait_for_timeout(2000)
#         page.evaluate("() => document.fonts.ready")

#         page.add_style_tag(content="""
#             html, body {
#                 margin: 0 !important;
#                 padding: 0 !important;
#             }
#             .pagebreakbefore {
#                 break-before: page;
#                 page-break-before: always;
#             }
#         """)

#         tenant_config = PDF_CONFIG.get(tenant, PDF_CONFIG["default"])
#         config = tenant_config.get(format_, tenant_config.get("A4"))

#         if not config:
#             raise HTTPException(status_code=400, detail=f"No config found for {format_}")

#         page.pdf(
#             path=output,
#             format=format_,
#             print_background=True,
#             margin=config["margin"],
#             prefer_css_page_size=True
#         )

#         browser.close()
#         return output


# @app.get("/generate-pdf")
# async def generate_pdf_api(
#     url: str = Query(..., description="URL of the HTML page"),
#     tenant: str = Query("default", description="Tenant name (multi-tenant configs)")
# ):
#     """
#     Converts a given HTML page to PDF.
#     Auto-detects format from URL like '::A4' or '::A5'.
#     Uses config.json for margins (multi-tenant).
#     """
#     match = re.search(r"::(A\d+)", url)
#     if not match:
#         raise HTTPException(status_code=400, detail="Format (A4, A5, etc.) not found in URL")

#     format_ = match.group(1)
#     output_filename = f"{tenant}_{format_}.pdf"
    
#     # Run sync playwright in thread pool
#     loop = asyncio.get_event_loop()
#     pdf_path = await loop.run_in_executor(
#         executor, 
#         generate_pdf_sync, 
#         format_, 
#         url, 
#         output_filename, 
#         tenant
#     )
    
#     return FileResponse(pdf_path, filename=output_filename, media_type="application/pdf")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000)



import re
import json
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()
	
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config.json
CONFIG_PATH = Path(__file__).parent / "config.json"
default_config = {
    "default": {
        "A4": {"margin": {"top": "30px", "right": "0px", "bottom": "30px", "left": "0px"}},
        "A5": {"margin": {"top": "5mm", "right": "0mm", "bottom": "5mm", "left": "0mm"}}
    }
}
try:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                PDF_CONFIG = json.loads(content)
            else:
                print("⚠️ config.json is empty, using default config")
                PDF_CONFIG = default_config
    else:
        print("⚠️ config.json not found, using default config")
        PDF_CONFIG = default_config
except Exception as e:
    print(f"⚠️ Error loading config.json: {e}. Falling back to default config.")
    PDF_CONFIG = default_config


# Thread pool for running sync playwright
executor = ThreadPoolExecutor(max_workers=3)


# def generate_pdf_sync(format_: str, url: str, output: str, tenant: str):
#     """Synchronous version of generate_pdf using sync_playwright"""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
        
#         print(f"📄 Loading URL: {url}")
        
#         # Use same settings as your working script
#         page.goto(url, wait_until="networkidle")
#         page.wait_for_timeout(2000)
#         page.evaluate("() => document.fonts.ready")
        
#         print(f"✅ Page loaded successfully")
        
#         # Add custom styles
#         page.add_style_tag(content="""
#             html, body {
#                 margin: 0 !important;
#                 padding: 0 !important;
#             }
#             .pagebreakbefore {
#                 break-before: page;
#                 page-break-before: always;
#             }
#         """)

#         # Get tenant-specific config
#         tenant_config = PDF_CONFIG.get(tenant, PDF_CONFIG["default"])
#         config = tenant_config.get(format_, tenant_config.get("A4"))

#         if not config:
#             browser.close()
#             raise HTTPException(status_code=400, detail=f"No config found for {format_}")

#         print(f"📋 PDF Config: format={format_}, margin={config['margin']}")
        
#         # Generate PDF with same settings as your working script
#         page.pdf(
#             path=output,
#             format=format_,
#             print_background=True,
#             margin=config["margin"],
#             prefer_css_page_size=True
#         )

#         browser.close()
#         print(f"✅ PDF generated successfully: {output}")
#         return output

#perfectly working but saves pdf on server
def generate_pdf_sync_main(format_: str, url: str, output: str, tenant: str):
    """Synchronous version of generate_pdf using sync_playwright"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        )
        page = browser.new_page()
        
        print(f"📄 Loading URL: {url}")
        
        try:
            # Navigate and wait
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(2000)
            
            # Check if page has content
            content = page.content()
            print(f"📝 Page content length: {len(content)} characters")
            
            if len(content) < 100:
                print("⚠️ Warning: Page content seems too short!")
            
            # Wait for fonts
            page.evaluate("() => document.fonts.ready")
            page.wait_for_timeout(1000)  # Extra wait after fonts
            
            print(f"✅ Page loaded successfully")
            
            # Add custom styles
            page.add_style_tag(content="""
                html, body {
                    margin: 0 !important;
                    padding: 0 !important;
                }
                .pagebreakbefore {
                    break-before: page;
                    page-break-before: always;
                }
                @page :first {
                    margin-top: 0 !important;
                }
            """)

            # Get tenant-specific config
            tenant_config = PDF_CONFIG.get(tenant, PDF_CONFIG["default"])
            config = tenant_config.get(format_, tenant_config.get("A4"))

            if not config:
                browser.close()
                raise HTTPException(status_code=400, detail=f"No config found for {format_}")

            print(f"📋 PDF Config: format={format_}, margin={config['margin']}")
            
            # Generate PDF
            page.pdf(
                path=output,
                format=format_,
                print_background=True,
                margin=config["margin"],
                prefer_css_page_size=True
            )

            print(f"✅ PDF generated successfully: {output}")
            
        except Exception as e:
            print(f"❌ Error during PDF generation: {str(e)}")
            raise
        finally:
            browser.close()
            
        return output


def generate_pdf_sync(format_: str, url: str, tenant: str):
    """Synchronous version of generate_pdf using sync_playwright - returns PDF bytes"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        )
        page = browser.new_page()
        
        print(f"📄 Loading URL: {url}")
        
        try:
            # Navigate and wait
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(2000)
            
            # Check if page has content
            content = page.content()
            print(f"📝 Page content length: {len(content)} characters")
            
            if len(content) < 100:
                print("⚠️ Warning: Page content seems too short!")
            
            # Wait for fonts
            page.evaluate("() => document.fonts.ready")
            page.wait_for_timeout(1000)
            
            print(f"✅ Page loaded successfully")
            
            # Add custom styles
            page.add_style_tag(content="""
                html, body {
                    margin: 0 !important;
                    padding: 0 !important;
                }
                .pagebreakbefore {
                    break-before: page;
                    page-break-before: always;
                }
                @page :first {
                    margin-top: 0 !important;
                }
            """)

            # Get tenant-specific config
            tenant_config = PDF_CONFIG.get(tenant, PDF_CONFIG["default"])
            config = tenant_config.get(format_, tenant_config.get("A4"))

            if not config:
                browser.close()
                raise HTTPException(status_code=400, detail=f"No config found for {format_}")

            print(f"📋 PDF Config: format={format_}, margin={config['margin']}")
            
            # Generate PDF and return bytes instead of saving to file
            pdf_bytes = page.pdf(
                format=format_,
                print_background=True,
                margin=config["margin"],
                prefer_css_page_size=True
            )

            print(f"✅ PDF generated successfully")
            
        except Exception as e:
            print(f"❌ Error during PDF generation: {str(e)}")
            raise
        finally:
            browser.close()
            
        return pdf_bytes
    
# @app.get("/generate-pdf-main") #this is the main
# async def generate_pdf_api_main(
#     url: str = Query(..., description="URL of the HTML page"),
#     tenant: str = Query("default", description="Tenant name (multi-tenant configs)")
# ):
#     """
#     Converts a given HTML page to PDF.
#     Auto-detects format from URL like '::A4' or '::A5'.
#     Uses config.json for margins (multi-tenant).
#     """
#     match = re.search(r"::(A\d+)", url)
#     if not match:
#         raise HTTPException(status_code=400, detail="Format (A4, A5, etc.) not found in URL")

#     format_ = match.group(1)
#     output_filename = f"{tenant}_{format_}.pdf"
    
#     print(f"🚀 Starting PDF generation: format={format_}, tenant={tenant}")
    
#     try:
#         # Run sync playwright in thread pool
#         loop = asyncio.get_event_loop()
#         pdf_path = await loop.run_in_executor(
#             executor, 
#             generate_pdf_sync, 
#             format_, 
#             url, 
#             output_filename, 
#             tenant
#         )
        
#         return FileResponse(pdf_path, filename=output_filename, media_type="application/pdf")
    
#     except Exception as e:
#         print(f"❌ Error: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.get("/generate-pdf")
async def generate_pdf_api(
    url: str = Query(..., description="URL of the HTML page"),
    tenant: str = Query("default", description="Tenant name (multi-tenant configs)")
):
    """
    Converts a given HTML page to PDF.
    Auto-detects format from URL like '::A4' or '::A5'.
    Uses config.json for margins (multi-tenant).
    """
    match = re.search(r"::(A\d+)", url)
    if not match:
        raise HTTPException(status_code=400, detail="Format (A4, A5, etc.) not found in URL")

    format_ = match.group(1)
    output_filename = f"{tenant}_{format_}.pdf"
    
    print(f"🚀 Starting PDF generation: format={format_}, tenant={tenant}")
    
    try:
        # Run sync playwright in thread pool
        loop = asyncio.get_event_loop()
        pdf_bytes = await loop.run_in_executor(
            executor, 
            generate_pdf_sync, 
            format_, 
            url, 
            tenant
        )
        
        from fastapi.responses import Response
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{output_filename}"'
            }
        )
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "ok",
        "service": "web-to-pdf-generator",
        "uptime": "running"
    }
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)