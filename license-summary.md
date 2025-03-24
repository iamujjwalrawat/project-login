
### Summary of Cloud-Native Principles

This application structure and code adhere to the following cloud-native principles:

1. **Codebase**: Single codebase for the application.
2. **Dependencies**: Explicitly declared in `package.json`.
3. **Config**: Configuration is managed through environment variables.
4. **Backing Services**: Treat services like databases as attached resources.
5. **Build, Release, Run**: Separate stages for building and running the application.
6. **Processes**: Execute the application as stateless processes.
7. **Port Binding**: The application binds to a port for HTTP services.
8. **Concurrency**: Scale out the application by running multiple processes.
9. **Disposability**: Processes start quickly and shut down gracefully.
10. **Dev/Prod Parity**: Keep development and production environments similar.
11. **Logs**: Treat logs as event streams for centralized logging.
12. **Admin Processes**: Run administrative tasks as one-off processes.

### Conclusion

This complete setup provides a cloud-native web application that is scalable, maintainable, and efficient. You can further enhance it by integrating a real backend API for authentication and user management.