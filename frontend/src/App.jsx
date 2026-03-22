import { Suspense, lazy } from 'react';
import { Routes, Route, NavLink } from 'react-router-dom';

const KnowledgeGraph = lazy(() => import('./views/KnowledgeGraph'));

function RouteFallback() {
  return (
    <div className="min-h-[420px] flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mx-auto mb-4" />
        <p className="text-sm text-gray-500">页面加载中...</p>
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Academic Evolution Graph</h1>
          <p className="text-sm text-gray-500">面向数学主题演化分析的静态知识图谱与证据分层展示</p>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex space-x-8">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                `py-4 px-2 border-b-2 font-medium text-sm ${
                  isActive
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`
              }
            >
              演化知识图谱
            </NavLink>
            <NavLink
              to="/knowledge-graph"
              className={({ isActive }) =>
                `py-4 px-2 border-b-2 font-medium text-sm ${
                  isActive
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`
              }
            >
              Demo 视图
            </NavLink>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <Suspense fallback={<RouteFallback />}>
          <Routes>
            <Route path="/" element={<KnowledgeGraph />} />
            <Route path="/knowledge-graph" element={<KnowledgeGraph />} />
          </Routes>
        </Suspense>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <p className="text-center text-sm text-gray-500">
            Academic Evolution Graph - Data: {new Date().toLocaleDateString()}
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
