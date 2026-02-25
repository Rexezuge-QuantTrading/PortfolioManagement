import { APIGatewayProxyHandler } from 'aws-lambda';
import { router } from '@/api/router';

export const api: APIGatewayProxyHandler = async (event, context) => {
  return router(event, context);
};
