exports.hello = async (_event: never) => {
  return {
    statusCode: 200,
    body: JSON.stringify({
      message: 'Go Serverless v4! Your function executed successfully!',
    }),
  };
};
