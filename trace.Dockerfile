FROM mcr.microsoft.com/playwright:v1.40.0-jammy

# Set working directory as build argument with default value
ARG WORKDIR=/traces
WORKDIR ${WORKDIR}

# Expose port 9323 which is the default port for Playwright trace viewer
EXPOSE 9323

# Command to start the Playwright trace viewer
# Usage: docker run -p 9323:9323 -v $(pwd)/test-results:/traces --build-arg WORKDIR=/custom/path trace-viewer <trace-file>
# Then open http://localhost:9323 in your browser
ENTRYPOINT ["playwright", "show-trace"]
CMD ["trace.zip"]