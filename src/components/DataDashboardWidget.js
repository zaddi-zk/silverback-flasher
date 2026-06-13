import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useCallback, useEffect, useMemo, useState } from 'react';
import styles from './DataDashboardWidget.module.css';
const categoryLabels = {
    sales: 'Sales',
    engagement: 'Engagement',
    traffic: 'Traffic',
    risk: 'Risk'
};
const categoryAccent = {
    sales: '#1d4ed8',
    engagement: '#059669',
    traffic: '#c026d3',
    risk: '#b91c1c'
};
const accessibleFormat = (value) => new Intl.NumberFormat('en-US', {
    maximumFractionDigits: value % 1 === 0 ? 0 : 1
}).format(value);
const getChangeLabel = (change) => change === 0 ? 'No change' : change > 0 ? `${change}% increase` : `${Math.abs(change)}% decrease`;
const statusCopy = {
    idle: 'Metrics are up to date.',
    loading: 'Loading latest signals.',
    error: 'Unable to load dashboard metrics.'
};
function useDebouncedValue(value, delay = 180) {
    const [debouncedValue, setDebouncedValue] = useState(value);
    useEffect(() => {
        const id = window.setTimeout(() => setDebouncedValue(value), delay);
        return () => window.clearTimeout(id);
    }, [value, delay]);
    return debouncedValue;
}
const MetricCard = ({ item }) => {
    const trendPositive = item.change >= 0;
    return (_jsxs("article", { className: styles.metricCard, "aria-label": `${item.label} metric`, children: [_jsxs("div", { className: styles.metricHeader, children: [_jsx("span", { className: styles.metricLabel, children: item.label }), _jsx("span", { className: styles.metricCategory, style: { color: categoryAccent[item.category] }, children: categoryLabels[item.category] })] }), _jsxs("div", { className: styles.metricBody, children: [_jsx("p", { className: styles.metricValue, children: accessibleFormat(item.value) }), _jsxs("p", { className: `${styles.metricChange} ${trendPositive ? styles.positive : styles.negative}`, children: [trendPositive ? '▲' : '▼', " ", getChangeLabel(item.change)] })] })] }));
};
const TrendChart = ({ data }) => {
    const maxAmount = useMemo(() => Math.max(...data.map((item) => Math.abs(item.value)), 1), [data]);
    return (_jsx("div", { className: styles.chartWrapper, "aria-label": "Trend overview chart", children: _jsx("div", { className: styles.chartGrid, children: data.map((item) => {
                const height = Math.max(12, Math.round((Math.abs(item.value) / maxAmount) * 100));
                return (_jsxs("div", { className: styles.chartBarShell, children: [_jsx("div", { className: styles.chartBar, style: { height: `${height}%`, backgroundColor: categoryAccent[item.category] } }), _jsx("span", { className: styles.chartBarLabel, children: item.label })] }, item.id));
            }) }) }));
};
const DataDashboardWidget = ({ data, status, primaryLabel = 'Dashboard snapshot', errorMessage }) => {
    const [selectedCategory, setSelectedCategory] = useState('all');
    const [detailOpen, setDetailOpen] = useState(false);
    const selectedLabel = selectedCategory === 'all' ? 'All categories' : categoryLabels[selectedCategory];
    const filteredData = useMemo(() => (selectedCategory === 'all' ? data : data.filter((item) => item.category === selectedCategory)), [data, selectedCategory]);
    const totalItems = filteredData.length;
    const totalImpact = useMemo(() => filteredData.reduce((sum, item) => sum + item.value, 0), [filteredData]);
    const averageChange = useMemo(() => (totalItems ? filteredData.reduce((sum, item) => sum + item.change, 0) / totalItems : 0), [filteredData, totalItems]);
    const debouncedData = useDebouncedValue(filteredData, 140);
    useEffect(() => {
        if (status === 'error') {
            setDetailOpen(false);
        }
    }, [status]);
    const handleCategoryClick = useCallback((category) => {
        setSelectedCategory(category);
        setDetailOpen(true);
    }, []);
    const handleKeyDown = useCallback((event) => {
        if (event.key === 'Escape' && detailOpen) {
            setDetailOpen(false);
            event.stopPropagation();
        }
    }, [detailOpen]);
    return (_jsxs("section", { className: styles.widgetShell, "aria-labelledby": "dashboard-widget-heading", onKeyDown: handleKeyDown, children: [_jsxs("div", { className: styles.widgetHeader, children: [_jsxs("div", { children: [_jsx("p", { className: styles.widgetEyebrow, children: "Live overview" }), _jsx("h2", { id: "dashboard-widget-heading", className: styles.widgetTitle, children: primaryLabel })] }), _jsx("div", { className: styles.statusPill, role: "status", "aria-live": "polite", children: statusCopy[status] })] }), _jsxs("div", { className: styles.widgetBody, children: [_jsxs("aside", { className: styles.filterPanel, "aria-label": "Category filters", children: [_jsx("p", { className: styles.filterHeading, children: "Category filter" }), _jsxs("div", { className: styles.filterList, role: "radiogroup", "aria-label": "Select metric category", children: [_jsx("button", { type: "button", className: `${styles.filterItem} ${selectedCategory === 'all' ? styles.activeFilter : ''}`, "aria-checked": selectedCategory === 'all', role: "radio", onClick: () => handleCategoryClick('all'), children: "All" }), ['sales', 'engagement', 'traffic', 'risk'].map((category) => (_jsx("button", { type: "button", className: `${styles.filterItem} ${selectedCategory === category ? styles.activeFilter : ''}`, "aria-checked": selectedCategory === category, role: "radio", onClick: () => handleCategoryClick(category), children: categoryLabels[category] }, category)))] }), _jsxs("div", { className: styles.summaryCard, "aria-label": "Filtered metrics summary", children: [_jsx("p", { className: styles.summaryTitle, children: selectedLabel }), _jsxs("dl", { children: [_jsxs("div", { className: styles.summaryRow, children: [_jsx("dt", { children: "Metrics" }), _jsx("dd", { children: totalItems })] }), _jsxs("div", { className: styles.summaryRow, children: [_jsx("dt", { children: "Total amount" }), _jsx("dd", { children: accessibleFormat(totalImpact) })] }), _jsxs("div", { className: styles.summaryRow, children: [_jsx("dt", { children: "Average trend" }), _jsxs("dd", { children: [averageChange.toFixed(1), "%"] })] })] })] })] }), _jsx("div", { className: styles.contentArea, children: status === 'loading' ? (_jsxs("div", { className: styles.stateCard, role: "status", "aria-live": "polite", children: [_jsx("div", { className: styles.loader, "aria-hidden": "true" }), _jsx("p", { children: "Fetching recent performance signals\u2026" })] })) : status === 'error' ? (_jsxs("div", { className: styles.stateCard, role: "alert", children: [_jsx("p", { className: styles.stateTitle, children: "Something went wrong" }), _jsx("p", { children: errorMessage ?? 'Unable to load widget data. Retry or contact support.' })] })) : debouncedData.length === 0 ? (_jsxs("div", { className: styles.stateCard, role: "status", "aria-live": "polite", children: [_jsx("p", { className: styles.stateTitle, children: "No metrics available" }), _jsx("p", { children: "Try expanding to a different category or refreshing the data source." })] })) : (_jsxs("div", { className: styles.dashboardGrid, children: [_jsx("div", { className: styles.metricGrid, children: debouncedData.map((item) => (_jsx(MetricCard, { item: item }, item.id))) }), _jsxs("div", { className: styles.chartCard, "aria-label": "Metric trend bar chart", children: [_jsxs("div", { className: styles.chartHeader, children: [_jsx("p", { className: styles.chartTitle, children: "Trend snapshot" }), _jsx("button", { type: "button", className: styles.toggleButton, "aria-expanded": detailOpen, onClick: () => setDetailOpen((current) => !current), children: detailOpen ? 'Hide details' : 'Show details' })] }), _jsx(TrendChart, { data: debouncedData }), _jsx("div", { className: `${styles.detailPanel} ${detailOpen ? styles.detailOpen : ''}`, children: _jsx("p", { className: styles.detailText, children: detailOpen
                                                    ? 'Each bar shows the relative scale of the selected metrics for the active category. Use the filters to compare sales, engagement, traffic, and risk trends.'
                                                    : 'Open details for guidance and interpretation.' }) })] })] })) })] })] }));
};
export default DataDashboardWidget;
