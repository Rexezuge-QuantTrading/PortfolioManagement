import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';

export const router = async (event: APIGatewayProxyEvent, _context: Context): Promise<APIGatewayProxyResult> => {
  // Lambda Function URL uses different event structure than API Gateway
  const httpMethod =
    (event as APIGatewayProxyEvent & { requestContext?: { http?: { method: string } } }).requestContext?.http?.method || event.httpMethod;
  const path = (event as APIGatewayProxyEvent & { rawPath?: string }).rawPath || event.path;
  console.log('Request:', { httpMethod, path });

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
  };

  if (httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: corsHeaders,
      body: '',
    };
  }

  try {
    const result: APIGatewayProxyResult = {
      statusCode: 200,
      headers: corsHeaders,
      body: JSON.stringify({ message: 'Hello world' }),
    };

    return {
      ...result,
      headers: { ...result.headers, ...corsHeaders },
    };
  } catch (error) {
    console.error('Router error:', error);
    return {
      statusCode: 500,
      headers: corsHeaders,
      body: JSON.stringify({ error: 'Internal Server Error' }),
    };
  }
};
