FROM microsoft/dotnet:2.0-sdk
WORKDIR /app

# Copy csproj and restore as distinct layers
COPY *.csproj ./
RUN dotnet restore
COPY . ./
WORKDIR /app
ENTRYPOINT ["dotnet", "test"]
