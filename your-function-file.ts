// Deno Edge Function: Admin Login Proxy

// Triggering redeploy after environment secret update - You can remove this line after this deployment.

// Import the Deno standard library module for serving HTTP requests.
import { serve } from "https://deno.land/std@0.190.0/http/server.ts";

// Retrieve the Flattern Admin Login URL from environment variables.
// This variable was set as a GitHub Secret and should now be accessible.
const FLATTERN_ADMIN_LOGIN_URL = Deno.env.get("FLATTERN_ADMIN_LOGIN_URL");

// Start the HTTP server. This function will be called for every incoming request.
serve(async (req: Request) => {
  // 1. Check if the environment variable is set
  if (!FLATTERN_ADMIN_LOGIN_URL) {
    console.error("FLATTERN_ADMIN_LOGIN_URL environment variable is not set.");
    return new Response(
      JSON.stringify({ error: "Server configuration error: Admin login URL missing." }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }

  // 2. Only allow POST requests for the login proxy
  if (req.method !== "POST") {
    return new Response(
      JSON.stringify({ error: "Method Not Allowed. Only POST requests are accepted." }),
      { status: 405, headers: { "Content-Type": "application/json" } },
    );
  }

  // 3. Ensure the request has a JSON content type
  const contentType = req.headers.get("content-type");
  if (!contentType || !contentType.includes("application/json")) {
    return new Response(
      JSON.stringify({ error: "Bad Request: Content-Type must be application/json." }),
      { status: 400, headers: { "Content-Type": "application/json" } },
    );
  }

  try {
    // 4. Parse the incoming request body as JSON
    const requestBody = await req.json();

    // 5. Forward the request to the actual Flattern admin login endpoint
    const flatternResponse = await fetch(FLATTERN_ADMIN_LOGIN_URL, {
      method: "POST", // Always POST to the target
      headers: {
        "Content-Type": "application/json",
        // Add any other necessary headers from the original request if needed,
        // but often for a simple proxy, just Content-Type is enough.
      },
      body: JSON.stringify(requestBody), // Send the original JSON body
    });

    // 6. Get the response body and status from the Flattern server
    const responseData = await flatternResponse.json();
    const responseStatus = flatternResponse.status;
    const responseHeaders = new Headers();
    responseHeaders.set("Content-Type", "application/json");

    // Optionally, you might want to forward specific headers from flatternResponse
    // For example:
    // const setCookie = flatternResponse.headers.get("set-cookie");
    // if (setCookie) {
    //   responseHeaders.set("set-cookie", setCookie);
    // }

    // 7. Return the response from the Flattern server back to the client
    return new Response(
      JSON.stringify(responseData),
      { status: responseStatus, headers: responseHeaders },
    );
  } catch (error) {
    console.error("Error processing request:", error);
    return new Response(
      JSON.stringify({ error: "Internal Server Error during proxy request." }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }
});
