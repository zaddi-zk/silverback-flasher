import DataDashboardWidget, { DashboardItem } from './DataDashboardWidget';
import styles from './LandingPage.module.css';

const widgetData: DashboardItem[] = [
  { id: 'a1', label: 'Revenue', value: 12740, change: 12, category: 'sales' },
  { id: 'b2', label: 'Transactions', value: 1283, change: -4, category: 'sales' },
  { id: 'c3', label: 'New users', value: 964, change: 9, category: 'engagement' },
  { id: 'd4', label: 'Conversion rate', value: 7.6, change: 0.7, category: 'engagement' },
  { id: 'e5', label: 'Active sessions', value: 4321, change: 3, category: 'traffic' },
  { id: 'f6', label: 'Churn risk', value: 4.2, change: -1.4, category: 'risk' }
];

const wallets = [
  { ticker: 'BTC', label: 'Bitcoin', details: 'Native BTC settlement, low fees, 3 confirmations' },
  { ticker: 'ETH', label: 'Ethereum', details: 'ERC-20 settlement with verified contract support' },
  { ticker: 'LTC', label: 'Litecoin', details: 'Trusted LTC routing for fast finality' },
  { ticker: 'USDT', label: 'Tether ERC-20', details: 'Stable settlement on Ethereum with ERC-20 support' }
];

const promises = [
  { title: 'Fast bridge timing', description: 'Average processed time 5-15 minutes after payment confirmation.' },
  { title: 'Clear wallet support', description: 'Only BTC, ETH, LTC, and USDT ERC-20 are accepted to avoid chain confusion.' },
  { title: 'Admin mark-as-paid', description: 'Every transaction is reviewed and marked paid by our operations team to ensure settlement.' }
];

const amountPromises = [
  { tier: 'Basic', amount: '$50 – $500', price: '$10 – $30', description: 'Test flash, small wallet transactions' },
  { tier: 'Standard', amount: '$1,000 – $5,000', price: '$50 – $150', description: 'Medium wallet bridging' },
  { tier: 'Pro', amount: '$10,000 – $50,000', price: '$200 – $500', description: 'High-value cross-chain flips' },
  { tier: 'Enterprise', amount: '$100,000 – $500,000+', price: '$1,000+', description: 'Institutional-grade bridging' }
];

const timePromises = [
  { phase: 'Payment confirmation', timeframe: '5 – 15 minutes', expectation: 'Waiting for blockchain confirmations' },
  { phase: 'Bridge execution', timeframe: '1 – 5 minutes', expectation: 'Funds moved across chains' },
  { phase: 'Settlement', timeframe: '< 30 seconds', expectation: "Funds arrive in user's wallet" },
  { phase: 'Total', timeframe: '6 – 20 minutes', expectation: 'From payment to funds received' }
];

const guarantees = [
  { title: 'Zero slippage', description: 'You get exactly the amount you paid for' },
  { title: 'No fees hidden', description: 'Bridge fee is shown upfront' },
  { title: 'Refund policy', description: 'If the flash fails, refund issued within 24 hours' },
  { title: 'Explorer verification', description: 'TX hash provided for each transaction' }
];

const testimonials = [
  {
    quote: 'Silverback delivered the fastest cross-chain settlement we have ever seen. No delays, no ambiguity.',
    author: 'Ava R., DeFi Growth Lead'
  },
  {
    quote: 'The bot walkthrough felt seamless, and support responded instantly when I needed help.',
    author: 'Noah K., Crypto Operations Manager'
  },
  {
    quote: 'A modern bridge experience with enterprise-level reliability and real-time clarity.',
    author: 'Priya S., Blockchain Strategist'
  }
];

const LandingPage = () => {
  return (
    <div className={styles.pageShell}>
      <header className={styles.heroSection}>
        <div className={styles.heroCopy}>
          <p className={styles.heroLabel}>Silverback Flasher</p>
          <h1 className={styles.heroTitle}>Flash liquidity across chains with instant, enterprise-grade precision.</h1>
          <p className={styles.heroDescription}>
            Smart bridge settlement, real-time confirmations, and 24/7 support built for traders, funds, and DeFi teams. Supported wallets: BTC, ETH, LTC, USDT ERC-20. Start in Telegram and finish with a secure bridge workflow that never stalls.
          </p>
          <div className={styles.heroActions}>
            <a
              className={styles.primaryButton}
              href="https://t.me/SilverFlasher_bot"
              target="_blank"
              rel="noreferrer noopener"
            >
              Click here to start the bridge bot
            </a>
            <a className={styles.secondaryButton} href="#features">
              Explore the platform
            </a>
          </div>
          <div className={styles.metricStrip} aria-label="Performance snapshot">
            <div>
              <p className={styles.metricValue}>99.9%</p>
              <p className={styles.metricLabel}>Availability</p>
            </div>
            <div>
              <p className={styles.metricValue}><span>2</span> min</p>
              <p className={styles.metricLabel}>Average response</p>
            </div>
            <div>
              <p className={styles.metricValue}>24/7</p>
              <p className={styles.metricLabel}>Support access</p>
            </div>
          </div>
        </div>

        <aside className={styles.heroVisual} aria-label="Dashboard preview">
          <div className={styles.productCard}>
            <p className={styles.cardEyebrow}>Live dashboard preview</p>
            <DataDashboardWidget data={widgetData} status="idle" primaryLabel="Landing page insights" />
          </div>
        </aside>
      </header>

      <section className={styles.section} id="features" aria-labelledby="features-heading">
        <div className={styles.sectionHeading}>
          <p className={styles.sectionPreheading}>Why choose Silverback</p>
          <h2 id="features-heading">Built for fast-moving crypto teams and careful enterprise flows.</h2>
        </div>
        <div className={styles.featureGrid}>
          <article className={styles.featureCard}>
            <h3>Guaranteed instant settlement</h3>
            <p>Flash every supported network with a resilient protocol that minimizes latency and maximizes finality.</p>
          </article>
          <article className={styles.featureCard}>
            <h3>Smart bot guidance</h3>
            <p>The Telegram bot handles your flow from onboarding to TX verification, preventing stale states and broken paths.</p>
          </article>
          <article className={styles.featureCard}>
            <h3>Modern support hub</h3>
            <p>Active support, real-time follow-ups, and documentation links keep every user on the fastest route to success.</p>
          </article>
          <article className={styles.featureCard}>
            <h3>Enterprise-grade visibility</h3>
            <p>Every transaction is recorded, monitored, and surfaced clearly so there is zero ambiguity in status updates.</p>
          </article>
        </div>
      </section>

      <section className={styles.section} id="wallets" aria-labelledby="wallets-heading">
        <div className={styles.sectionHeading}>
          <p className={styles.sectionPreheading}>Supported wallets</p>
          <h2 id="wallets-heading">Only the wallets we support, no guesswork.</h2>
        </div>
        <div className={styles.featureGrid}>
          {wallets.map((item) => (
            <article key={item.ticker} className={styles.featureCard}>
              <h3>{item.ticker} - {item.label}</h3>
              <p>{item.details}</p>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.section} id="amount-promises" aria-labelledby="amount-promises-heading">
        <div className={styles.sectionHeading}>
          <p className={styles.sectionPreheading}>💰 Amount Promises</p>
          <h2 id="amount-promises-heading">Tiered flash sizing with predictable value.</h2>
        </div>
        <div className={styles.promiseGrid}>
          {amountPromises.map((item) => (
            <article key={item.tier} className={styles.promiseCard}>
              <p className={styles.promiseTier}>{item.tier}</p>
              <p className={styles.promiseValue}>{item.amount}</p>
              <p className={styles.promisePrice}>{item.price}</p>
              <p className={styles.promiseDesc}>{item.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.section} id="time-promises" aria-labelledby="time-promises-heading">
        <div className={styles.sectionHeading}>
          <p className={styles.sectionPreheading}>⏱️ Time Promises</p>
          <h2 id="time-promises-heading">Clear timing expectations for every stage.</h2>
        </div>
        <div className={styles.timeGrid}>
          {timePromises.map((item) => (
            <article key={item.phase} className={styles.timeRow}>
              <div className={styles.timeCell}>
                <p className={styles.timePhase}>{item.phase}</p>
              </div>
              <div className={styles.timeCell}>
                <p className={styles.timeFrame}>{item.timeframe}</p>
              </div>
              <div className={styles.timeCell}>
                <p className={styles.timeExpectation}>{item.expectation}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.section} id="guarantees" aria-labelledby="guarantees-heading">
        <div className={styles.sectionHeading}>
          <p className={styles.sectionPreheading}>✅ Guarantees a user expects</p>
          <h2 id="guarantees-heading">We keep the bridge simple, visible, and reliable.</h2>
        </div>
        <p className={styles.guaranteeIntro}>
          "We guarantee the flash will go through within 20 minutes, or you get a full refund."
        </p>
        <div className={styles.guaranteeGrid}>
          {guarantees.map((item) => (
            <article key={item.title} className={styles.guaranteeCard}>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.section} id="promise" aria-labelledby="promise-heading">
        <div className={styles.sectionHeading}>
          <p className={styles.sectionPreheading}>Flash promise</p>
          <h2 id="promise-heading">Fast, transparent, and backed by our verification workflow.</h2>
        </div>
        <div className={styles.featureGrid}>
          {promises.map((item) => (
            <article key={item.title} className={styles.featureCard}>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.testimonialSection} aria-labelledby="testimonial-heading">
        <div className={styles.testimonialHeading}>
          <p className={styles.sectionPreheading}>Trusted by pro operators</p>
          <h2 id="testimonial-heading">Active testimonials from teams using Silverback.</h2>
        </div>
        <div className={styles.testimonialGrid}>
          {testimonials.map((item) => (
            <blockquote key={item.author} className={styles.testimonialCard}>
              <p>{item.quote}</p>
              <footer>{item.author}</footer>
            </blockquote>
          ))}
        </div>
      </section>

      <section className={styles.supportSection} aria-labelledby="support-heading">
        <div className={styles.supportContent}>
          <div>
            <p className={styles.sectionPreheading}>Support engineered for urgency</p>
            <h2 id="support-heading">Modern support built into every bridge.</h2>
            <p>
              Instant bot routing, enterprise response times, and a dedicated fallback path for high-priority issues. Users immediately know where to go and how to resolve any bridge edge case.
            </p>
          </div>
          <div className={styles.supportCard}>
            <p className={styles.supportLabel}>Contact</p>
            <p className={styles.supportDetail}>Telegram: <a href="https://t.me/SilverFlasher_bot">@SilverFlasher_bot</a></p>
            <p className={styles.supportDetail}>Email: <a href="mailto:support@hottboiihitzz.cc">support@hottboiihitzz.cc</a></p>
            <p className={styles.supportDetail}>Docs: <a href="https://hottboiihitzz.cc">hottboiihitzz.cc</a></p>
          </div>
        </div>
      </section>

      <footer className={styles.footer}>
        <p>Silverback Flasher - the most reliable flash settlement layer for modern crypto teams.</p>
        <a href="https://t.me/SilverFlasher_bot">Start the bot</a>
      </footer>
    </div>
  );
};

export default LandingPage;
