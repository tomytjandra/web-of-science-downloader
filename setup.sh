mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = false\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml