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

export function papersForConcept(conceptId: string): GraphNode[] {
  const paperIds = new Set(
    graph.edges
      .filter((e) => e.to === conceptId || e.from === conceptId)
      .flatMap((e) => [e.from, e.to])
  );
  return graph.nodes.filter((n) => n.nodeType === "papers" && paperIds.has(n.id));
}

export default graph;
