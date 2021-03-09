FROM nginx
# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy api config
COPY nginx.conf /etc/nginx/conf.d/