release: chmod u+x release.sh && ./release.sh
web: uvicorn bsl_menu.main:app --proxy-headers --host=0.0.0.0 --port=${PORT}