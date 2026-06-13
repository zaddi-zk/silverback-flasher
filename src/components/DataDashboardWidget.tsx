import { useCallback, useEffect, useMemo, useState } from 'react';
import styles from './DataDashboardWidget.module.css';

export type RangeKey = 'weekly' | 'monthly' | 'quarterly';

export type DashboardItem = {
  id: string;
  label: string;
  value: number;
  change: number;
  category: 'sales' | 'engagement' | 'traffic' | 'risk';
};

export type WidgetStatus = 'idle' | 'loading' | 'error';

const categoryLabels: Record<DashboardItem['category'], string> = {
  sales: 'Sales',
  engagement: 'Engagement',
  traffic: 'Traffic',
  risk: 'Risk'
};

const categoryAccent: Record<DashboardItem['category'], string> = {
  sales: '#1d4ed8',
  engagement: '#059669',
  traffic: '#c026d3',
  risk: '#b91c1c'
};

const accessibleFormat = (value: number) =>
  new Intl.NumberFormat('en-US', {
    maximumFractionDigits: value % 1 === 0 ? 0 : 1
  }).format(value);

const getChangeLabel = (change: number) =>
  change === 0 ? 'No change' : change > 0 ? `${change}% increase` : `${Math.abs(change)}% decrease`;

const statusCopy: Record<WidgetStatus, string> = {
  idle: 'Metrics are up to date.',
  loading: 'Loading latest signals.',
  error: 'Unable to load dashboard metrics.'
};

type DataDashboardWidgetProps = {
  data: DashboardItem[];
  status: WidgetStatus;
  primaryLabel?: string;
  errorMessage?: string;
};

function useDebouncedValue<T>(value: T, delay = 180) {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const id = window.setTimeout(() => setDebouncedValue(value), delay);
    return () => window.clearTimeout(id);
  }, [value, delay]);

  return debouncedValue;
}

const MetricCard = ({ item }: { item: DashboardItem }) => {
  const trendPositive = item.change >= 0;
  return (
    <article className={styles.metricCard} aria-label={`${item.label} metric`}>
      <div className={styles.metricHeader}>
        <span className={styles.metricLabel}>{item.label}</span>
        <span className={styles.metricCategory} style={{ color: categoryAccent[item.category] }}>
          {categoryLabels[item.category]}
        </span>
      </div>
      <div className={styles.metricBody}>
        <p className={styles.metricValue}>{accessibleFormat(item.value)}</p>
        <p className={`${styles.metricChange} ${trendPositive ? styles.positive : styles.negative}`}>
          {trendPositive ? '▲' : '▼'} {getChangeLabel(item.change)}
        </p>
      </div>
    </article>
  );
};

const TrendChart = ({ data }: { data: DashboardItem[] }) => {
  const maxAmount = useMemo(() => Math.max(...data.map((item) => Math.abs(item.value)), 1), [data]);

  return (
    <div className={styles.chartWrapper} aria-label="Trend overview chart">
      <div className={styles.chartGrid}>
        {data.map((item) => {
          const height = Math.max(12, Math.round((Math.abs(item.value) / maxAmount) * 100));
          return (
            <div key={item.id} className={styles.chartBarShell}>
              <div className={styles.chartBar} style={{ height: `${height}%`, backgroundColor: categoryAccent[item.category] }} />
              <span className={styles.chartBarLabel}>{item.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const DataDashboardWidget = ({ data, status, primaryLabel = 'Dashboard snapshot', errorMessage }: DataDashboardWidgetProps) => {
  const [selectedCategory, setSelectedCategory] = useState<DashboardItem['category'] | 'all'>('all');
  const [detailOpen, setDetailOpen] = useState(false);

  const selectedLabel = selectedCategory === 'all' ? 'All categories' : categoryLabels[selectedCategory];
  const filteredData = useMemo(
    () => (selectedCategory === 'all' ? data : data.filter((item) => item.category === selectedCategory)),
    [data, selectedCategory]
  );

  const totalItems = filteredData.length;
  const totalImpact = useMemo(() => filteredData.reduce((sum, item) => sum + item.value, 0), [filteredData]);
  const averageChange = useMemo(
    () => (totalItems ? filteredData.reduce((sum, item) => sum + item.change, 0) / totalItems : 0),
    [filteredData, totalItems]
  );

  const debouncedData = useDebouncedValue(filteredData, 140);

  useEffect(() => {
    if (status === 'error') {
      setDetailOpen(false);
    }
  }, [status]);

  const handleCategoryClick = useCallback((category: DashboardItem['category'] | 'all') => {
    setSelectedCategory(category);
    setDetailOpen(true);
  }, []);

  const handleKeyDown = useCallback((event: React.KeyboardEvent<HTMLDivElement>) => {
    if (event.key === 'Escape' && detailOpen) {
      setDetailOpen(false);
      event.stopPropagation();
    }
  }, [detailOpen]);

  return (
    <section className={styles.widgetShell} aria-labelledby="dashboard-widget-heading" onKeyDown={handleKeyDown}>
      <div className={styles.widgetHeader}>
        <div>
          <p className={styles.widgetEyebrow}>Live overview</p>
          <h2 id="dashboard-widget-heading" className={styles.widgetTitle}>{primaryLabel}</h2>
        </div>
        <div className={styles.statusPill} role="status" aria-live="polite">
          {statusCopy[status]}
        </div>
      </div>

      <div className={styles.widgetBody}>
        <aside className={styles.filterPanel} aria-label="Category filters">
          <p className={styles.filterHeading}>Category filter</p>
          <div className={styles.filterList} role="radiogroup" aria-label="Select metric category">
            <button
              type="button"
              className={`${styles.filterItem} ${selectedCategory === 'all' ? styles.activeFilter : ''}`}
              aria-checked={selectedCategory === 'all'}
              role="radio"
              onClick={() => handleCategoryClick('all')}
            >
              All
            </button>
            {(['sales', 'engagement', 'traffic', 'risk'] as DashboardItem['category'][]).map((category) => (
              <button
                key={category}
                type="button"
                className={`${styles.filterItem} ${selectedCategory === category ? styles.activeFilter : ''}`}
                aria-checked={selectedCategory === category}
                role="radio"
                onClick={() => handleCategoryClick(category)}
              >
                {categoryLabels[category]}
              </button>
            ))}
          </div>

          <div className={styles.summaryCard} aria-label="Filtered metrics summary">
            <p className={styles.summaryTitle}>{selectedLabel}</p>
            <dl>
              <div className={styles.summaryRow}>
                <dt>Metrics</dt>
                <dd>{totalItems}</dd>
              </div>
              <div className={styles.summaryRow}>
                <dt>Total amount</dt>
                <dd>{accessibleFormat(totalImpact)}</dd>
              </div>
              <div className={styles.summaryRow}>
                <dt>Average trend</dt>
                <dd>{averageChange.toFixed(1)}%</dd>
              </div>
            </dl>
          </div>
        </aside>

        <div className={styles.contentArea}>
          {status === 'loading' ? (
            <div className={styles.stateCard} role="status" aria-live="polite">
              <div className={styles.loader} aria-hidden="true" />
              <p>Fetching recent performance signals…</p>
            </div>
          ) : status === 'error' ? (
            <div className={styles.stateCard} role="alert">
              <p className={styles.stateTitle}>Something went wrong</p>
              <p>{errorMessage ?? 'Unable to load widget data. Retry or contact support.'}</p>
            </div>
          ) : debouncedData.length === 0 ? (
            <div className={styles.stateCard} role="status" aria-live="polite">
              <p className={styles.stateTitle}>No metrics available</p>
              <p>Try expanding to a different category or refreshing the data source.</p>
            </div>
          ) : (
            <div className={styles.dashboardGrid}>
              <div className={styles.metricGrid}>
                {debouncedData.map((item) => (
                  <MetricCard key={item.id} item={item} />
                ))}
              </div>

              <div className={styles.chartCard} aria-label="Metric trend bar chart">
                <div className={styles.chartHeader}>
                  <p className={styles.chartTitle}>Trend snapshot</p>
                  <button
                    type="button"
                    className={styles.toggleButton}
                    aria-expanded={detailOpen}
                    onClick={() => setDetailOpen((current) => !current)}
                  >
                    {detailOpen ? 'Hide details' : 'Show details'}
                  </button>
                </div>
                <TrendChart data={debouncedData} />
                <div className={`${styles.detailPanel} ${detailOpen ? styles.detailOpen : ''}`}>
                  <p className={styles.detailText}>
                    {detailOpen
                      ? 'Each bar shows the relative scale of the selected metrics for the active category. Use the filters to compare sales, engagement, traffic, and risk trends.'
                      : 'Open details for guidance and interpretation.'}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default DataDashboardWidget;
