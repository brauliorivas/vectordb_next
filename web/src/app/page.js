import Products from "@/components/products";

const API_URL = process.env.API_URL ?? 'http://localhost:8000';

async function getData() {
  const res = await fetch(`${API_URL}/products`, { cache: 'no-store' });

  if (!res.ok) {
    throw new Error('Failed to fetch data');
  }

  return res.json();
}

export default async function Home() {
  const data = await getData();

  return (
    <main>
      <header>Ecommerce</header>

      <Products data={data} api={API_URL} />
    </main>
  );
}
