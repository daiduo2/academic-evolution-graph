.PHONY: help deploy clean install frontend-install test evolution-analysis math-benchmark math-lo-benchmark math-ag-benchmark kg-export kg-visualization

help:
	@echo "Academic Trend Monitor - 可用命令:"
	@echo ""
	@echo "  make install          - 安装 Python 依赖"
	@echo "  make frontend-install - 安装前端依赖"
	@echo "  make test             - 运行测试"
	@echo "  make evolution-analysis - 运行历史主题演化分析"
	@echo "  make math-benchmark   - 运行统一 Math 基准检查 (math_lo + math_ag)"
	@echo "  make math-lo-benchmark - 运行 Math.LO 基准检查"
	@echo "  make math-ag-benchmark - 运行 Math.AG 基准检查"
	@echo "  make kg-export        - 生成 baseline / preview KG"
	@echo "  make kg-visualization - 生成知识图谱前端 bundle"
	@echo "  make deploy           - 部署到 GitHub Pages"
	@echo "  make clean            - 清理生成的数据"
	@echo ""

install:
	pip install -r requirements.txt

frontend-install:
	cd frontend && npm install

test:
	pytest tests/test_evolution_analysis.py tests/test_math_kg_visualization_export.py -q

evolution-analysis:
	@echo "运行历史主题演化分析..."
	python3 pipeline/evolution_analysis.py
	@echo "分析完成，结果已生成到 data/output/"

math-benchmark:
	@echo "运行统一 Math benchmark..."
	python3 pipeline/math_benchmark.py --domain math_lo
	python3 pipeline/math_benchmark.py --domain math_ag
	@echo "统一 Math benchmark 完成，结果已生成到 data/output/benchmarks/"

math-lo-benchmark:
	@echo "运行 Math.LO benchmark..."
	python3 pipeline/math_lo_benchmark.py
	@echo "Math.LO benchmark 完成，结果已生成到 data/output/benchmarks/math_lo/"

math-ag-benchmark:
	@echo "运行 Math.AG benchmark..."
	python3 pipeline/math_ag_benchmark.py
	@echo "Math.AG benchmark 完成，结果已生成到 data/output/benchmarks/math_ag/"

kg-export:
	@echo "生成 baseline KG..."
	python3 pipeline/math_kg_export.py --input data/output/aligned_topics_hierarchy.json --benchmark-lo docs/plans/2026-03-12-math-lo-benchmark.md --benchmark-ag docs/plans/2026-03-18-math-ag-benchmark.md --output-dir data/output/kg_v1
	@echo "生成 PR conditional KG..."
	python3 pipeline/math_kg_export.py --input data/output/aligned_topics_hierarchy.json --benchmark-lo docs/plans/2026-03-12-math-lo-benchmark.md --benchmark-ag docs/plans/2026-03-18-math-ag-benchmark.md --benchmark-pr docs/plans/2026-03-21-math-pr-case-curation.md --output-dir data/output/kg_v1_pr_conditional

kg-visualization:
	@echo "生成知识图谱前端 bundle..."
	python3 pipeline/math_kg_visualization_export.py --input-dir data/output/kg_v1 --output-dir data/output/kg_v1_visualization
	python3 pipeline/math_kg_visualization_export.py --input-dir data/output/kg_v1_pr_conditional --output-dir data/output/kg_v1_pr_conditional_visualization

deploy:
	@echo "构建前端并部署..."
	@mkdir -p frontend/public/data frontend/public/data/output frontend/public/data/weekly frontend/public/data/analysis/daily
	@cp data/output/*.json frontend/public/data/ || echo "No data files yet"
	@cp data/output/*.json frontend/public/data/output/ || echo "No output data files yet"
	@rm -rf frontend/public/data/output/kg_v1_visualization frontend/public/data/output/kg_v1_pr_conditional_visualization
	@mkdir -p frontend/public/data/output/kg_v1_visualization frontend/public/data/output/kg_v1_pr_conditional_visualization
	@cp -r data/output/kg_v1_visualization/. frontend/public/data/output/kg_v1_visualization/ || echo "No baseline KG bundle yet"
	@cp -r data/output/kg_v1_pr_conditional_visualization/. frontend/public/data/output/kg_v1_pr_conditional_visualization/ || echo "No preview KG bundle yet"
	@mkdir -p frontend/public/data/evolution_case_detail
	@cp -r data/output/evolution_case_detail/. frontend/public/data/evolution_case_detail/ || echo "No evolution case detail yet"
	cd frontend && npm run build
	@echo "构建完成。请推送代码触发 GitHub Actions 自动部署。"

clean:
	@echo "清理生成的数据..."
	rm -rf data/output/*.json
	rm -rf data/output/evolution_case_detail
	rm -f data/output/evolution_report.md
	rm -rf data/output/kg_v1
	rm -rf data/output/kg_v1_visualization
	rm -rf data/output/kg_v1_pr_conditional
	rm -rf data/output/kg_v1_pr_conditional_visualization
	rm -rf pipeline/__pycache__
	rm -rf frontend/dist
	@echo "清理完成"
