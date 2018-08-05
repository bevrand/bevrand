using System;
using System.IO;
using System.Reflection;
using bevrand.authenticationapi.Data;
using bevrand.authenticationapi.Middleware;
using bevrand.authenticationapi.Repository;
using bevrand.authenticationapi.Services;
using bevrand.authenticationapi.Services.Interfaces;
using OpenTracing.Util;
using Jaeger;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Swashbuckle.AspNetCore.Swagger;


namespace bevrand.authenticationapi
{
    public class Startup
    {
        private static readonly ILoggerFactory LoggerFactory = new LoggerFactory().AddConsole();
        private static readonly Tracer Tracer = Tracing.Init("Authenication Api", LoggerFactory);
        
        public Startup(IHostingEnvironment env)
        {
            var builder = new ConfigurationBuilder()
                .SetBasePath(env.ContentRootPath)
                .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
                .AddJsonFile($"appsettings.{env.EnvironmentName}.json", optional: true);
            
            Console.WriteLine(env.EnvironmentName);    
            builder.AddEnvironmentVariables();
            Configuration = builder.Build();
        }
        

        public IConfiguration Configuration { get; }


        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            var sqlConnectionString = Configuration.GetConnectionString("PostGres");
            Console.WriteLine(sqlConnectionString);
            services.AddDbContext<UserContext>(options =>
                options.UseNpgsql(sqlConnectionString));
            services.AddScoped<IUserRepository, UserRepository>();
            services.AddScoped<IUsersLogic, UsersLogic>();
            services.AddScoped<IValidationLogic, ValidationLogic>();
  
            services.AddMvc();
            
            //TODO Reconsider using the "GlobalTracer" / "AddOpenTracing", this is probably the cause of a lot of noise in the tracing.
            GlobalTracer.Register(Tracer);
            services.AddOpenTracing();
            
                // Register the Swagger generator, defining one or more Swagger documents
            services.AddSwaggerGen(c =>
            {
                var baseDirectory = AppDomain.CurrentDomain.BaseDirectory;
                var commentsFileName = Assembly.GetExecutingAssembly().GetName().Name + ".XML";
                var commentsFile = Path.Combine(baseDirectory, commentsFileName);
                
                c.SwaggerDoc("v1", new Info { Title = "Authentication Api", Version = "v1" });
                c.IncludeXmlComments(commentsFile);
            });
        }
        

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseMiddleware(typeof(ErrorHandlingMiddleware));
          //  app.UseMiddleware(typeof(TracingHandlingMiddleware));

            app.UseSwagger();

            // Enable middleware to serve swagger-ui (HTML, JS, CSS, etc.), specifying the Swagger JSON endpoint.
            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint("/swagger/v1/swagger.json", "Authentication Api");
            });

            app.UseMvc();
        }
    }
}

