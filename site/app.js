// Conciliamus Architecture Knowledge Graph - Obsidian Workspace
let network = null;
let nodesDataSet = null;
let edgesDataSet = null;
let activeNodeId = null;
let physicsActive = true;
let currentFilter = 'all';
let graphData = null;

const typeTheme = {
  'Architecture Concept': { bg: '#8b5cf6', border: '#a78bfa', text: '#ddd6fe' },
  'iFlow Specification': { bg: '#10b981', border: '#34d399', text: '#a7f3d0' },
  'Decision Record': { bg: '#f59e0b', border: '#fbbf24', text: '#fde68a' },
  'Data Contract': { bg: '#06b6d4', border: '#22d3ee', text: '#a5f3fc' },
  'Test Evidence': { bg: '#f43f5e', border: '#fb7185', text: '#fecdd3' },
  'Presentation Concept': { bg: '#d946ef', border: '#f0abfc', text: '#f5d0fe' },
  'UI Concept': { bg: '#e11d48', border: '#fb7185', text: '#ffe4e6' },
  'Architecture FAQ': { bg: '#64748b', border: '#94a3b8', text: '#cbd5e1' }
};

async function loadGraphData() {
  if (window.EMBEDDED_GRAPH_DATA) {
    return window.EMBEDDED_GRAPH_DATA;
  }
  try {
    const res = await fetch('/graph?format=json');
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn('Could not fetch /graph?format=json, checking local fallback', err);
  }
  try {
    const res = await fetch('../graph/knowledge-graph.json');
    if (res.ok) {
      return await res.json();
    }
  } catch (e) {}
  return null;
}

async function initGraph() {
  graphData = await loadGraphData();
  if (!graphData || !graphData.nodes) {
    console.error('Failed to load graph data');
    return;
  }

  const hdrNodeCount = document.getElementById('hdrNodeCount');
  const hdrEdgeCount = document.getElementById('hdrEdgeCount');
  if (hdrNodeCount) hdrNodeCount.innerText = graphData.nodes.length;
  if (hdrEdgeCount) hdrEdgeCount.innerText = graphData.edges.length;

  const container = document.getElementById('network');

  const visNodes = graphData.nodes.map(n => {
    const theme = typeTheme[n.type] || { bg: '#6366f1', border: '#818cf8', text: '#e0e7ff' };
    const degree = n.degree || 1;
    const size = Math.max(10, Math.min(26, 8 + Math.sqrt(degree) * 4.5));

    return {
      id: n.id,
      label: n.label,
      shape: 'dot',
      size: size,
      color: {
        background: theme.bg,
        border: theme.border,
        highlight: { background: '#f59e0b', border: '#fbbf24' },
        hover: { background: theme.border, border: '#ffffff' }
      },
      borderWidth: 2,
      font: {
        color: '#cbd5e1',
        size: 11,
        face: 'Inter, sans-serif',
        strokeWidth: 2,
        strokeColor: '#0f1117',
        vadjust: 3
      },
      raw: n
    };
  });

  const visEdges = graphData.edges.map(e => ({
    id: e.source + '-->' + e.target,
    from: e.source,
    to: e.target,
    label: e.relation,
    arrows: { to: { enabled: true, scaleFactor: 0.45 } },
    color: {
      color: 'rgba(148, 163, 184, 0.22)',
      highlight: '#f59e0b',
      hover: '#a78bfa'
    },
    font: {
      color: '#64748b',
      size: 9,
      face: 'JetBrains Mono',
      background: '#111116',
      strokeWidth: 0
    },
    smooth: { type: 'continuous', roundness: 0.2 }
  }));

  nodesDataSet = new vis.DataSet(visNodes);
  edgesDataSet = new vis.DataSet(visEdges);

  const options = {
    nodes: { scaling: { min: 10, max: 30 } },
    physics: {
      solver: 'forceAtlas2Based',
      forceAtlas2Based: {
        gravitationalConstant: -75,
        centralGravity: 0.012,
        springLength: 135,
        springConstant: 0.08,
        damping: 0.45
      },
      stabilization: { iterations: 150 }
    },
    interaction: {
      hover: true,
      tooltipDelay: 150,
      hoverConnectedEdges: true,
      keyboard: false
    }
  };

  network = new vis.Network(container, { nodes: nodesDataSet, edges: edgesDataSet }, options);

  network.on('click', function(params) {
    if (params.nodes.length > 0) {
      selectNode(params.nodes[0]);
    } else {
      clearDimming();
    }
  });

  network.on('doubleClick', function(params) {
    if (params.nodes.length > 0) {
      network.focus(params.nodes[0], { scale: 1.4, animation: { duration: 600, easingFunction: 'easeInOutQuad' } });
    }
  });

  // Global event delegation for data-jump and data-tag buttons
  document.addEventListener('click', function(e) {
    const jumpBtn = e.target.closest('[data-jump]');
    if (jumpBtn) {
      const targetId = jumpBtn.getAttribute('data-jump');
      if (targetId) {
        jumpToNode(targetId);
        closeSearchDropdown();
      }
      return;
    }

    const tagBtn = e.target.closest('[data-tag]');
    if (tagBtn) {
      const tag = tagBtn.getAttribute('data-tag');
      if (tag) searchByTag(tag);
      return;
    }
  });

  setTimeout(() => {
    selectNode('architecture/dual-iflow-pattern');
  }, 400);
}

function selectNode(nodeId) {
  if (!graphData) return;
  activeNodeId = nodeId;
  const node = graphData.nodes.find(n => n.id === nodeId);
  if (!node) return;

  network.selectNodes([nodeId]);
  dimUnconnected(nodeId);
  renderNote(node);
  expandNotePane();
}

function dimUnconnected(centerNodeId) {
  const connectedNodeIds = new Set(network.getConnectedNodes(centerNodeId));
  connectedNodeIds.add(centerNodeId);

  const updates = [];
  nodesDataSet.forEach(n => {
    const isConnected = connectedNodeIds.has(n.id);
    const theme = typeTheme[n.raw.type] || { bg: '#6366f1', border: '#818cf8' };

    if (n.id === centerNodeId) {
      updates.push({
        id: n.id,
        color: { background: '#f59e0b', border: '#fef08a' },
        borderWidth: 4,
        font: { color: '#ffffff', size: 12 }
      });
    } else if (isConnected) {
      updates.push({
        id: n.id,
        color: { background: theme.bg, border: theme.border },
        borderWidth: 2,
        font: { color: '#f1f5f9', size: 11 }
      });
    } else {
      updates.push({
        id: n.id,
        color: { background: '#242430', border: '#333342' },
        borderWidth: 1,
        font: { color: '#475569', size: 9 }
      });
    }
  });
  nodesDataSet.update(updates);

  const edgeUpdates = [];
  edgesDataSet.forEach(e => {
    const isConn = (e.from === centerNodeId || e.to === centerNodeId);
    edgeUpdates.push({
      id: e.id,
      color: { color: isConn ? '#f59e0b' : 'rgba(51, 65, 85, 0.15)' },
      width: isConn ? 2 : 1
    });
  });
  edgesDataSet.update(edgeUpdates);
}

function clearDimming() {
  activeNodeId = null;
  const updates = [];
  nodesDataSet.forEach(n => {
    const theme = typeTheme[n.raw.type] || { bg: '#6366f1', border: '#818cf8' };
    updates.push({
      id: n.id,
      color: { background: theme.bg, border: theme.border },
      borderWidth: 2,
      font: { color: '#cbd5e1', size: 11 }
    });
  });
  nodesDataSet.update(updates);

  const edgeUpdates = [];
  edgesDataSet.forEach(e => {
    edgeUpdates.push({
      id: e.id,
      color: { color: 'rgba(148, 163, 184, 0.22)' },
      width: 1
    });
  });
  edgesDataSet.update(edgeUpdates);
}

async function renderNote(node) {
  const noteBreadcrumb = document.getElementById('noteBreadcrumb');
  const noteTitle = document.getElementById('noteTitle');
  const noteId = document.getElementById('noteId');
  const noteDomain = document.getElementById('noteDomain');
  const noteDegreeText = document.getElementById('noteDegreeText');
  const noteStatusText = document.getElementById('noteStatusText');
  const noteGithubLink = document.getElementById('noteGithubLink');

  if (noteBreadcrumb) noteBreadcrumb.innerText = 'knowledge' + node.path;
  if (noteTitle) noteTitle.innerText = node.label;
  if (noteId) noteId.innerText = node.id;
  if (noteDomain) noteDomain.innerText = node.domain || 'Architektur & Integration';
  if (noteDegreeText) noteDegreeText.innerText = '🔗 ' + (node.degree || 0) + ' verknüpfte Relationen im OKF-Graphen';

  const theme = typeTheme[node.type] || { bg: '#8b5cf6', text: '#ddd6fe' };
  const typeBadge = document.getElementById('noteTypeBadge');
  if (typeBadge) {
    typeBadge.innerText = node.type;
    typeBadge.style.background = theme.bg + '33';
    typeBadge.style.color = theme.text;
    typeBadge.style.borderColor = theme.bg;
  }

  if (noteStatusText) noteStatusText.innerText = node.status || 'VERIFIED';
  if (noteGithubLink) noteGithubLink.href = 'https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/knowledge' + node.path;

  const tagsEl = document.getElementById('noteTags');
  if (tagsEl) {
    tagsEl.innerHTML = (node.tags || []).map(t =>
      '<button data-tag="' + t + '" class="px-2 py-0.5 rounded-full bg-[#242436] hover:bg-purple-900/60 hover:text-purple-300 text-slate-300 text-[10px] border border-[#36364e] transition font-mono">#' + t + '</button>'
    ).join('');
  }

  renderBacklinks(node.id);

  let markdownBody = '';
  try {
    const resp = await fetch('/concepts/' + encodeURIComponent(node.id));
    if (resp.ok) {
      const json = await resp.json();
      markdownBody = json.content;
    }
  } catch (err) {}

  if (!markdownBody && window.EMBEDDED_NOTES && window.EMBEDDED_NOTES[node.id]) {
    markdownBody = window.EMBEDDED_NOTES[node.id].body;
  }

  if (!markdownBody) {
    markdownBody = '### ' + node.label + '\n\n' + (node.description || 'Dokumentation für dieses Konzept im OKF-Wissensbundle.') + '\n\n*Pfad: `knowledge' + node.path + '`*';
  }

  if (window.marked) {
    marked.setOptions({
      gfm: true,
      breaks: true,
      highlight: function(code, lang) {
        if (lang && window.hljs && hljs.getLanguage(lang)) {
          try { return hljs.highlight(code, { language: lang }).value; } catch (e) {}
        }
        if (window.hljs) return hljs.highlightAuto(code).value;
        return code;
      }
    });

    const mdContainer = document.getElementById('noteMarkdown');
    if (mdContainer) {
      mdContainer.innerHTML = marked.parse(markdownBody);

      mdContainer.querySelectorAll('a').forEach(a => {
        const href = a.getAttribute('href') || '';
        if (href.startsWith('/') || href.startsWith('../') || href.endsWith('.md')) {
          a.addEventListener('click', (e) => {
            e.preventDefault();
            const cleanTarget = href.replace(/^(\.\.\/|\/)/, '').replace(/\.md$/, '');
            const targetNode = graphData.nodes.find(n => n.id.endsWith(cleanTarget) || n.path.endsWith(cleanTarget + '.md'));
            if (targetNode) {
              network.focus(targetNode.id, { scale: 1.2, animation: { duration: 500, easingFunction: 'easeInOutQuad' } });
              selectNode(targetNode.id);
            }
          });
        }
      });
    }
  }
}

function renderBacklinks(nodeId) {
  if (!graphData) return;
  const incoming = graphData.edges.filter(e => e.target === nodeId);
  const outgoing = graphData.edges.filter(e => e.source === nodeId);

  const inCountEl = document.getElementById('inboundCount');
  const outCountEl = document.getElementById('outboundCount');
  if (inCountEl) inCountEl.innerText = incoming.length;
  if (outCountEl) outCountEl.innerText = outgoing.length;

  const inEl = document.getElementById('inboundLinks');
  if (inEl) {
    if (incoming.length === 0) {
      inEl.innerHTML = '<div class="text-slate-500 text-[11px] italic">Keine eingehenden Referenzen</div>';
    } else {
      inEl.innerHTML = incoming.map(e => {
        const srcNode = graphData.nodes.find(n => n.id === e.source);
        const title = srcNode ? srcNode.label : e.source;
        return '<button data-jump="' + e.source + '" class="w-full p-2 rounded-lg bg-[#1c1c28] hover:bg-[#262638] border border-[#2a2a3c] flex items-center justify-between text-left transition group">' +
          '<div class="flex items-center gap-2 truncate">' +
            '<span class="px-1.5 py-0.2 rounded text-[9px] font-mono uppercase bg-emerald-950/80 text-emerald-300 border border-emerald-800/60">[' + e.relation + ']</span>' +
            '<span class="text-xs text-slate-200 group-hover:text-purple-300 truncate">' + title + '</span>' +
          '</div>' +
          '<i class="fa-solid fa-arrow-turn-down text-[10px] text-slate-500 group-hover:text-purple-400 rotate-90 shrink-0 ml-2"></i>' +
        '</button>';
      }).join('');
    }
  }

  const outEl = document.getElementById('outboundLinks');
  if (outEl) {
    if (outgoing.length === 0) {
      outEl.innerHTML = '<div class="text-slate-500 text-[11px] italic">Keine ausgehenden Links</div>';
    } else {
      outEl.innerHTML = outgoing.map(e => {
        const tgtNode = graphData.nodes.find(n => n.id === e.target);
        const title = tgtNode ? tgtNode.label : e.target;
        return '<button data-jump="' + e.target + '" class="w-full p-2 rounded-lg bg-[#1c1c28] hover:bg-[#262638] border border-[#2a2a3c] flex items-center justify-between text-left transition group">' +
          '<div class="flex items-center gap-2 truncate">' +
            '<span class="px-1.5 py-0.2 rounded text-[9px] font-mono uppercase bg-purple-950/80 text-purple-300 border border-purple-800/60">[' + e.relation + ']</span>' +
            '<span class="text-xs text-slate-200 group-hover:text-purple-300 truncate">' + title + '</span>' +
          '</div>' +
          '<i class="fa-solid fa-arrow-turn-down text-[10px] text-slate-500 group-hover:text-purple-400 -rotate-90 shrink-0 ml-2"></i>' +
        '</button>';
      }).join('');
    }
  }
}

function jumpToNode(targetId) {
  if (!network) return;
  network.focus(targetId, { scale: 1.25, animation: { duration: 550, easingFunction: 'easeInOutQuad' } });
  selectNode(targetId);
}

function onSearch(term) {
  const clearBtn = document.getElementById('searchClear');
  const dropdown = document.getElementById('searchDropdown');
  if (!term || !graphData) {
    if (clearBtn) clearBtn.classList.add('hidden');
    if (dropdown) dropdown.classList.add('hidden');
    return;
  }

  const q = term.trim().toLowerCase();
  if (!q) {
    if (clearBtn) clearBtn.classList.add('hidden');
    if (dropdown) dropdown.classList.add('hidden');
    return;
  }

  if (clearBtn) clearBtn.classList.remove('hidden');
  const matches = graphData.nodes.filter(n =>
    n.label.toLowerCase().includes(q) ||
    n.id.toLowerCase().includes(q) ||
    (n.tags || []).some(t => t.toLowerCase().includes(q))
  );

  if (!dropdown) return;
  if (matches.length > 0) {
    dropdown.innerHTML = matches.slice(0, 7).map(m =>
      '<div data-jump="' + m.id + '" class="p-2.5 hover:bg-[#252538] border-b border-[#2c2c3e] cursor-pointer flex items-center justify-between transition">' +
        '<div>' +
          '<div class="font-medium text-white">' + m.label + '</div>' +
          '<div class="text-[10px] font-mono text-slate-400">' + m.id + '</div>' +
        '</div>' +
        '<span class="text-[9px] px-1.5 py-0.5 rounded font-mono uppercase bg-slate-800 text-slate-300 border border-slate-700">' + m.type + '</span>' +
      '</div>'
    ).join('');
    dropdown.classList.remove('hidden');
  } else {
    dropdown.innerHTML = '<div class="p-3 text-slate-500 text-center">Keine Übereinstimmung im Vault</div>';
    dropdown.classList.remove('hidden');
  }
}

function onSearchKey(event) {
  if (event.key === 'Enter') {
    const q = event.target.value.trim().toLowerCase();
    if (graphData) {
      const match = graphData.nodes.find(n => n.label.toLowerCase().includes(q) || n.id.toLowerCase().includes(q));
      if (match) {
        jumpToNode(match.id);
        closeSearchDropdown();
      }
    }
  } else if (event.key === 'Escape') {
    clearSearch();
  }
}

function clearSearch() {
  const input = document.getElementById('searchInput');
  if (input) input.value = '';
  const clearBtn = document.getElementById('searchClear');
  if (clearBtn) clearBtn.classList.add('hidden');
  closeSearchDropdown();
  resetView();
}

function closeSearchDropdown() {
  const dropdown = document.getElementById('searchDropdown');
  if (dropdown) dropdown.classList.add('hidden');
}

function searchByTag(tag) {
  const input = document.getElementById('searchInput');
  if (input) input.value = tag;
  onSearch(tag);
  if (graphData) {
    const matches = graphData.nodes.filter(n => (n.tags || []).includes(tag));
    if (matches.length > 0) {
      jumpToNode(matches[0].id);
    }
  }
}

function filterCategory(type, btn) {
  document.querySelectorAll('.filter-chip').forEach(b => {
    b.classList.remove('active', 'bg-purple-900/50', 'text-purple-300', 'border-purple-600');
    b.classList.add('bg-[#1a1a26]', 'text-slate-300', 'border-[#2e2e42]');
  });
  if (btn) {
    btn.classList.add('active', 'bg-purple-900/50', 'text-purple-300', 'border-purple-600');
    btn.classList.remove('bg-[#1a1a26]', 'text-slate-300', 'border-[#2e2e42]');
  }

  currentFilter = type;
  if (!nodesDataSet) return;
  if (type === 'all') {
    nodesDataSet.forEach(n => nodesDataSet.update({ id: n.id, hidden: false }));
  } else {
    nodesDataSet.forEach(n => {
      const isMatch = n.raw.type === type;
      nodesDataSet.update({ id: n.id, hidden: !isMatch });
    });
  }
  resetView();
}

function resetView() {
  if (network) network.fit({ animation: { duration: 600, easingFunction: 'easeInOutQuad' } });
}

function zoomIn() {
  if (!network) return;
  const scale = network.getScale();
  network.moveTo({ scale: scale * 1.3, animation: { duration: 300 } });
}

function zoomOut() {
  if (!network) return;
  const scale = network.getScale();
  network.moveTo({ scale: scale * 0.7, animation: { duration: 300 } });
}

function togglePhysics() {
  if (!network) return;
  physicsActive = !physicsActive;
  network.setOptions({ physics: { enabled: physicsActive } });
  const icon = document.getElementById('physicsIcon');
  const text = document.getElementById('physicsText');
  if (physicsActive) {
    if (icon) icon.className = 'fa-solid fa-pause text-amber-400';
    if (text) text.innerText = 'Physik Stop';
  } else {
    if (icon) icon.className = 'fa-solid fa-play text-emerald-400';
    if (text) text.innerText = 'Physik Start';
  }
}

function toggleFrontmatter() {
  const content = document.getElementById('fmContent');
  const icon = document.getElementById('fmToggleIcon');
  if (!content) return;
  if (content.classList.contains('hidden')) {
    content.classList.remove('hidden');
    if (icon) icon.classList.remove('rotate-180');
  } else {
    content.classList.add('hidden');
    if (icon) icon.classList.add('rotate-180');
  }
}

function collapseNotePane() {
  const pane = document.getElementById('notePane');
  const btn = document.getElementById('expandPaneBtn');
  if (pane) pane.classList.add('hidden');
  if (btn) btn.classList.remove('hidden');
}

function expandNotePane() {
  const pane = document.getElementById('notePane');
  const btn = document.getElementById('expandPaneBtn');
  if (pane) pane.classList.remove('hidden');
  if (btn) btn.classList.add('hidden');
}

function openObsidianModal() {
  const m = document.getElementById('obsidianModal');
  if (m) m.classList.remove('hidden');
}

function closeObsidianModal() {
  const m = document.getElementById('obsidianModal');
  if (m) m.classList.add('hidden');
}

function copyVaultPath() {
  const input = document.getElementById('vaultPathInput');
  if (!input) return;
  input.select();
  navigator.clipboard.writeText(input.value);
  const btnText = document.getElementById('copyBtnText');
  if (btnText) {
    btnText.innerText = 'Kopiert!';
    setTimeout(() => { btnText.innerText = 'Kopieren'; }, 2000);
  }
}

// Global functions for inline HTML event handlers
window.filterCategory = filterCategory;
window.resetView = resetView;
window.togglePhysics = togglePhysics;
window.openObsidianModal = openObsidianModal;
window.closeObsidianModal = closeObsidianModal;
window.copyVaultPath = copyVaultPath;
window.collapseNotePane = collapseNotePane;
window.expandNotePane = expandNotePane;
window.toggleFrontmatter = toggleFrontmatter;
window.onSearch = onSearch;
window.onSearchKey = onSearchKey;
window.clearSearch = clearSearch;
window.zoomIn = zoomIn;
window.zoomOut = zoomOut;

document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    const input = document.getElementById('searchInput');
    if (input) {
      input.focus();
      input.select();
    }
  }
  if (e.key === 'Escape') {
    closeObsidianModal();
    closeSearchDropdown();
  }
});

window.addEventListener('DOMContentLoaded', initGraph);
