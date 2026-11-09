import { randomUUID } from "node:crypto";

export function getServerSideProps({ res }) {
  res.setHeader("Cache-Control", "private, no-store");
  return { props: { sample: { release: "B", request: randomUUID(), renderedAt: new Date().toISOString() } } };
}

export default function Home({ sample }) {
  return <main><h1>Next.js SSR / rollback lab</h1><pre id="sample">{JSON.stringify(sample)}</pre></main>;
}
