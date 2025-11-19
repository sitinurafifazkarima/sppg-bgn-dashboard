mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@example.com\"\n\
\n\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
\n\
" > ~/.streamlit/config.toml
