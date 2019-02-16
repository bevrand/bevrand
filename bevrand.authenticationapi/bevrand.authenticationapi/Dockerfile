FROM microsoft/dotnet:2.2-sdk AS build-env
WORKDIR /app

# Copy csproj and restore as distinct layers
COPY *.csproj ./
RUN dotnet restore

# Copy everything else and build
COPY . ./
RUN dotnet publish -c Release -o out

# Build runtime image
FROM microsoft/dotnet:2.2-aspnetcore-runtime AS runtime
WORKDIR /app
EXPOSE 5000
COPY --from=build-env /app/out .

# Create a group and user
RUN addgroup --system --gid 4570 appgroup \
&& adduser --system -uid 4570 --ingroup appgroup --shell /bin/sh appuser
# Make app directory content read-only (dotnet is executed, not program)
RUN chown -R 4570:4570 ./ && chmod -R 0400 ./
# Drop user
USER appuser

ENTRYPOINT ["dotnet", "bevrand.authenticationapi.dll"]