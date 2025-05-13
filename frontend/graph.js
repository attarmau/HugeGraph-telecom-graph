fetch("http://localhost:8000/graph")
  .then(res => res.json())
  .then(data => drawGraph(data));

function drawGraph(data) {
  const svg = d3.select("svg");
  const width = window.innerWidth - 300;
  const height = window.innerHeight;

  const colorMap = {
    person: "#1f77b4",
    location: "#2ca02c",
    call: "#ff7f0e",
    call_event: "gray"
  };

  const simulation = d3.forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id(d => d.id).distance(120))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2));

  const link = svg.append("g")
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(data.links)
    .join("line")
    .attr("stroke", d => d.label === "made_at" ? "green" : "#999")
    .attr("stroke-dasharray", d => d.label === "made_at" ? "4" : "0")
    .attr("stroke-width", 2);

  const node = svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(data.nodes)
    .join("circle")
    .attr("r", 10)
    .attr("fill", d => colorMap[d.label] || "#ccc")
    .on("click", showNodeInfo)
    .call(drag(simulation));

  const label = svg.append("g")
    .selectAll("text")
    .data(data.nodes)
    .join("text")
    .attr("class", "node-label")
    .text(d => d.name || d.city || d.id || d.timestamp || d.block);

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);

    label
      .attr("x", d => d.x + 12)
      .attr("y", d => d.y + 4);
  });

  function drag(simulation) {
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }
    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }
    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
    return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
  }

  function showNodeInfo(event, d) {
    const details = document.getElementById("details");
    const props = Object.entries(d)
      .filter(([k]) => !["x", "y", "vx", "vy", "index"].includes(k))
      .map(([k, v]) => `<strong>${k}</strong>: ${v}`)
      .join("<br>");
    details.innerHTML = props;
  }
}
