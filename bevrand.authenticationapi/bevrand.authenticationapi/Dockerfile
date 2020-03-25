FROM mcr.microsoft.com/dotnet/core/sdk:3.1.200 AS build
WORKDIR /app

# Copy csproj and restore as distinct layers
COPY *.csproj ./
RUN dotnet restore

# Copy everything else and build
COPY . ./
RUN dotnet publish -c Release -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1.3 AS runtime
WORKDIR /app
EXPOSE 5000
COPY --from=build /app/out .
ENTRYPOINT ["dotnet", "bevrand.authenticationapi.dll"]
