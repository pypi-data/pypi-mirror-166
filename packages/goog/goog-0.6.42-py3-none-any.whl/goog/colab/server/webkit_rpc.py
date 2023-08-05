from unencryptedsocket import SS
from playwright.sync_api import sync_playwright
import threading
import time


def handle_popup(page):
    add_page_handlers(page)
    page.wait_for_load_state()


def add_page_handlers(page):
    page.on("popup", handle_popup)


def add_job(t, v):
    jobs[t] = v
    return True


def get_job_result(t):
    try:
        return job_results.pop(t)
    except:
        return KeyError()


jobs = {}
job_results = {}
with sync_playwright() as pw:
    driver = pw.webkit.launch(
        timeout=5000,
        headless=True,
    )
    context = driver.new_context(
        locale="en-US",
        timezone_id="America/Phoenix",
        viewport={"width": 1920, "height": 1200},
        ignore_https_errors=True,
        bypass_csp=True,
        color_scheme="dark",
    )
    page = context.new_page()
    add_page_handlers(page)
    page.goto("https://google.com/?q=colab")
    ss = SS(
        host="127.0.0.1",
        port='<sc_port>',
        silent=True,
        functions=dict(
            add_job=add_job,
            get_job_result=get_job_result,
        ),
    )
    p = threading.Thread(target=lambda: ss.start())
    p.daemon = True
    p.start()
    while True:
        try:
            t = next(iter(jobs.keys()))
            v = jobs.pop(t)
            name, args, kwargs = v
            method = page
            for name in name.split("."):
                method = getattr(method, name)
            r = method
            if callable(r):
                r = r(*args, **kwargs)
            job_results[t] = r
        except:
            time.sleep(1/1000)
    ss.stop()
    driver.close()

