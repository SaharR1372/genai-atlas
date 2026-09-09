// Thin typed accessor over site/src/data/graph.json, which scripts/build_graph.py
// compiles from data/**/*.yaml at the repo root. Regenerate with `npm run graph:build`
// (or `python3 scripts/build_graph.py` from the repo root) after editing any data file.
import graphData from "../data/graph.json";

export type GraphNode = {
  id: string;
  nodeType: string;
  label: string;
  sections: string[];
  tier: string | null;
  date: string | null;
  axes: Record<string, string[]> | null;
  data: Record<string, any>;
};

export type GraphEdge = {
  from: string;
  to: string;
  type: string;
  evidence: string | null;
  confidence: string | null;
  status: string | null;
};

export type Graph = {
  node_count: number;
  edge_count: number;
  nodes: GraphNode[];
  edges: GraphEdge[];
};

const graph = graphData as Graph;

export function allNodes(): GraphNode[] {
  return graph.nodes;
}

export function allEdges(): GraphEdge[] {
  return graph.edges;
}

export function nodesByType(nodeType: string): GraphNode[] {
  return graph.nodes.filter((n) => n.nodeType === nodeType);
}

export function nodeById(id: string): GraphNode | undefined {
  return graph.nodes.find((n) => n.id === id);
}

export function edgesFrom(id: string): GraphEdge[] {
  return graph.edges.filter((e) => e.from === id);
}

export function edgesTo(id: string): GraphEdge[] {
  return graph.edges.filter((e) => e.to === id);
}

export function conceptsByAxis(axis: string): GraphNode[] {
  return graph.nodes.filter((n) => n.nodeType === "concepts" && n.data.axis === axis);
}

const STATUS_ORDER = ["dominant", "ascendant", "contested", "emerging", "superseded"];

/** Research lines, ordered by how settled they are. */
export function allLines(): GraphNode[] {
  return graph.nodes
    .filter((n) => n.nodeType === "lines")
    .sort(
      (a, b) =>
        STATUS_ORDER.indexOf(a.data.status) - STATUS_ORDER.indexOf(b.data.status) ||
        (a.data.since ?? "").localeCompare(b.data.since ?? "")
    );
}

export function linesForSection(section: string): GraphNode[] {
  return allLines().filter((l) => (l.sections ?? []).includes(section));
}

export function papersInLine(lineId: string): GraphNode[] {
  return graph.nodes.filter(
    (n) => n.nodeType === "papers" && (n.data.lines ?? []).includes(lineId)
  );
}

export function allProblems(): GraphNode[] {
  return graph.nodes.filter((n) => n.nodeType === "problems");
}

export function allBenchmarks(): GraphNode[] {
  return graph.nodes.filter((n) => n.nodeType === "benchmarks");
}

/** Results for one benchmark, best value first (respecting higher_is_better). */
export function resultsForBenchmark(benchmarkId: string): GraphNode[] {
  const bench = nodeById(benchmarkId);
  const higherBetter = bench?.data.higher_is_better ?? false;
  return graph.nodes
    .filter((n) => n.nodeType === "results" && n.data.benchmark === benchmarkId)
    .sort((a, b) =>
      higherBetter ? b.data.value - a.data.value : a.data.value - b.data.value
    );
}

export function resultsForPaper(paperId: string): GraphNode[] {
  return graph.nodes.filter((n) => n.nodeType === "results" && n.data.paper === paperId);
}

/** Which line(s) a paper belongs to, as full nodes. */
export function linesOfPaper(paperId: string): GraphNode[] {
  const p = nodeById(paperId);
  return (p?.data.lines ?? []).map((id: string) => nodeById(id)).filter(Boolean) as GraphNode[];
}

/** Every paper with a date, oldest first — for the timeline. */
export function papersByDate(): GraphNode[] {
  return graph.nodes
    .filter((n) => n.nodeType === "papers" && n.date)
    .sort((a, b) => (a.date ?? "").localeCompare(b.date ?? ""));
}

export function papersForConcept(conceptId: string): GraphNode[] {
  const paperIds = new Set(
    graph.edges
      .filter((e) => e.to === conceptId || e.from === conceptId)
      .flatMap((e) => [e.from, e.to])
  );
  return graph.nodes.filter((n) => n.nodeType === "papers" && paperIds.has(n.id));
}

export default graph;
