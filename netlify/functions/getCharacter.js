const fetch = require("node-fetch");

exports.handler = async (event) => {
  const name = event.queryStringParameters.name;
  const publicKey = process.env.MARVEL_PUBLIC_KEY;
  const hash = process.env.MARVEL_HASH;
  const ts = 1;

  try {
    const response = await fetch(
      `https://gateway.marvel.com/v1/public/characters?name=${name}&ts=${ts}&apikey=${publicKey}&hash=${hash}`
    );
    const data = await response.json();

    return {
      statusCode: 200,
      body: JSON.stringify(data),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Failed to fetch character", error }),
    };
  }
};