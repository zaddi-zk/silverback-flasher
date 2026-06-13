import { useEffect, useMemo, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { AnimatePresence, motion } from 'framer-motion';
import { FaCheckCircle } from 'react-icons/fa';
import { BiChevronDown, BiChevronUp } from 'react-icons/bi';
import { FiExternalLink, FiRefreshCcw, FiShield } from 'react-icons/fi';

const trustItems = [
  '🔒 256-bit encrypted',
  '4,321 active sessions',
  '99.9% uptime'
];

const metrics = [
  { label: 'Total bridged', value: '$4,321,450' },
  { label: 'Active sessions', value: '1,247' },
  { label: 'Success rate', value: '99.9%' }
];

const features = [
  {
    title: 'Fast bridge execution',
    summary: 'Instant routing across supported networks',
    details: 'Move liquidity from one chain to another with enterprise-grade speed and monitoring.'
  },
  {
    title: 'Verified wallet support',
    summary: 'BTC, ETH, LTC, USDT ERC-20 only',
    details: 'Only proven wallets are supported to keep the bridge secure and predictable.'
  },
  {
    title: 'Direct operator monitoring',
    summary: 'Admin mark-as-paid workflow',
    details: 'Every transaction is reviewed for settlement and manually confirmed by the operations team.'
  },
  {
    title: 'Clear refund promise',
    summary: '20-minute settlement guarantee',
    details: 'If the flash fails to settle within 20 minutes, a full refund is issued within 24 hours.'
  }
];

const testimonials = [
  {
    name: 'Sarah K.',
    role: 'DeFi Trader',
    quote: 'Silverback delivered the fastest cross-chain settlement I’ve ever seen. The support team was responsive and the bridge completed within minutes.',
    avatar: 'https://i.pravatar.cc/150?img=1'
  },
  {
    name: 'Michael R.',
    role: 'Crypto Fund Manager',
    quote: 'The experience felt professional and secure. I trusted the payment promise and the transaction was verified instantly.',
    avatar: 'https://i.pravatar.cc/150?img=12'
  },
  {
    name: 'Elena V.',
    role: 'Blockchain Dev',
    quote: 'A strong product for large-value bridging. The promise page and guarantees made the flow very transparent.',
    avatar: 'https://i.pravatar.cc/150?img=18'
  }
];

const faqs = [
  {
    question: 'How long does a flash take?',
    answer: 'A full flash move takes 6-20 minutes from payment confirmation to final settlement, depending on network confirmation time.'
  },
  {
    question: 'What wallets do you support?',
    answer: 'Silverback Flasher supports BTC, ETH, LTC, and USDT ERC-20 only to reduce risk and ensure accurate settlement.'
  },
  {
    question: 'Is this legal?',
    answer: 'Yes — the service is built for professional operators and follows standard on-chain settlement practices.'
  }
];

const priceTiers = [
  { name: 'Basic', range: '$50 - $500 flash', fee: '$10 fee' },
  { name: 'Pro Flasher', range: '$150 - $5,000 flash', fee: '$35 fee' },
  { name: 'Enterprise', range: '$10,000 - $50,000 flash', fee: '$200 fee' }
];

function FeatureItem({ item, isOpen, onToggle }: { item: typeof features[0]; isOpen: boolean; onToggle: () => void }) {
  return (
    <div className="border border-slate-200 bg-white/90 shadow-soft rounded-[28px] p-5 transition hover:shadow-xl md:p-6">
      <button type="button" onClick={onToggle} className="flex w-full items-start justify-between gap-4 text-left">
        <div>
          <p className="text-base font-semibold text-slate-900">{item.title}</p>
          <p className="mt-3 text-sm leading-7 text-slate-600 md:text-base">{item.summary}</p>
        </div>
        <span className="text-primary md:hidden">{isOpen ? <BiChevronUp size={24} /> : <BiChevronDown size={24} />}</span>
      </button>
      <div className={`${isOpen ? 'mt-4 block' : 'hidden'} md:block`}>
        <p className="text-sm leading-7 text-slate-600">{item.details}</p>
      </div>
    </div>
  );
}

function TestimonialCard({ testimonial }: { testimonial: typeof testimonials[0] }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft"
    >
      <div className="flex items-center gap-4">
        <img src={testimonial.avatar} alt={testimonial.name} className="h-14 w-14 rounded-full object-cover" />
        <div>
          <div className="flex items-center gap-2 text-base font-semibold text-slate-900">
            {testimonial.name}
            <FaCheckCircle className="text-emerald-500" />
          </div>
          <p className="text-sm text-slate-500">{testimonial.role}</p>
        </div>
      </div>
      <p className="mt-5 text-sm leading-7 text-slate-700 md:text-base">“{testimonial.quote}”</p>
    </motion.article>
  );
}

function FAQItem({ faq, isOpen, onClick }: { faq: typeof faqs[0]; isOpen: boolean; onClick: () => void }) {
  return (
    <div className="border border-slate-200 bg-white/95 shadow-soft rounded-[28px]">
      <button type="button" onClick={onClick} className="flex w-full items-center justify-between gap-4 px-5 py-4 text-left">
        <span className="font-semibold text-slate-900">{faq.question}</span>
        <span className="text-primary">{isOpen ? <BiChevronUp size={24} /> : <BiChevronDown size={24} />}</span>
      </button>
      <div className={`${isOpen ? 'max-h-96 pb-5 px-5' : 'max-h-0 overflow-hidden'} transition-all duration-300`}>
        <p className="text-sm leading-7 text-slate-600">{faq.answer}</p>
      </div>
    </div>
  );
}

function TestimonialsSection() {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-primary">Customer confidence</p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">Trusted by real builders and funds.</h2>
        </div>
        <button
          type="button"
          onClick={() => setModalOpen(true)}
          className="inline-flex h-12 items-center justify-center rounded-full bg-secondary px-5 text-sm font-semibold text-white transition hover:bg-violet-600"
        >
          Read all testimonials
        </button>
      </div>

      <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
        {testimonials.map((item) => (
          <TestimonialCard key={item.name} testimonial={item} />
        ))}
      </div>

      <AnimatePresence>
        {modalOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 p-4"
          >
            <motion.div
              initial={{ y: 40, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: 40, opacity: 0 }}
              className="w-full max-w-3xl overflow-hidden rounded-[32px] bg-white p-6 shadow-soft"
            >
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.24em] text-primary">Full testimonials</p>
                  <h3 className="mt-2 text-2xl font-semibold text-slate-950">What operators say about Silverback.</h3>
                </div>
                <button type="button" onClick={() => setModalOpen(false)} className="text-slate-500 transition hover:text-slate-900">
                  Close
                </button>
              </div>
              <div className="mt-6 grid gap-4 lg:grid-cols-2">
                {testimonials.map((item) => (
                  <div key={item.name} className="rounded-[30px] border border-slate-200 bg-slate-50 p-5">
                    <div className="flex items-center gap-4">
                      <img src={item.avatar} alt={item.name} className="h-12 w-12 rounded-full object-cover" />
                      <div>
                        <div className="flex items-center gap-2 text-base font-semibold text-slate-900">
                          {item.name}
                          <FaCheckCircle className="text-emerald-500" />
                        </div>
                        <p className="text-sm text-slate-500">{item.role}</p>
                      </div>
                    </div>
                    <p className="mt-4 text-sm leading-7 text-slate-700">“{item.quote}”</p>
                  </div>
                ))}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}

function ProFlasherPage() {
  const navigate = useNavigate();
  const [timeLeft, setTimeLeft] = useState(899);
  const [deposit, setDeposit] = useState(85);
  const serviceFee = 35;
  const multiplier = 2.4;

  useEffect(() => {
    const timer = window.setInterval(() => {
      setTimeLeft((value) => (value > 0 ? value - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const formattedTime = useMemo(() => {
    const minutes = Math.floor(timeLeft / 60).toString().padStart(2, '0');
    const seconds = (timeLeft % 60).toString().padStart(2, '0');
    return `${minutes}:${seconds}`;
  }, [timeLeft]);

  const estimatedCapacity = useMemo(() => {
    return Math.max(0, deposit * multiplier).toFixed(0);
  }, [deposit]);

  const totalPayable = useMemo(() => {
    return (deposit + serviceFee).toFixed(2);
  }, [deposit]);

  const depositHint = deposit < 35 ? 'Minimum deposit is $35 to enable the Pro Flasher.' : `A $${deposit} deposit unlocks up to $${estimatedCapacity} in flash capacity.`;

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
      <Helmet>
        <title>Silverback Flasher – Pro Flasher</title>
      </Helmet>
      <div className="mx-auto max-w-6xl space-y-8">
        <div className="rounded-[36px] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm uppercase tracking-[0.24em] text-primary">Pro Flasher</p>
                  <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">Activate the pro bridge plan.</h1>
                  <p className="mt-2 text-sm text-slate-500">Time left: {formattedTime}</p>
                  <p className="mt-4 max-w-2xl text-base leading-8 text-slate-600 sm:text-lg">Start with a clear $35 service fee and see the actual flash capacity before you pay. This page makes the Pro Flasher flow actionable and click-ready.</p>
                </div>
            <button
              type="button"
              onClick={() => navigate('/')}
              className="inline-flex h-12 items-center justify-center rounded-full border border-slate-200 px-5 text-sm font-semibold text-slate-700 transition hover:bg-slate-100"
            >
              Back to home
            </button>
          </div>

          <div className="mt-8 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
            <div className="space-y-6 rounded-[32px] bg-slate-50 p-5 sm:p-6">
              <div className="rounded-[32px] border border-slate-200 bg-white p-6 shadow-sm">
                <p className="text-sm uppercase tracking-[0.24em] text-primary">Pro Flasher calculator</p>
                <div className="mt-6 space-y-4">
                  <label className="block text-sm font-semibold text-slate-900">Deposit amount</label>
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-slate-600">$</span>
                    <input
                      type="number"
                      min={35}
                      value={deposit}
                      onChange={(event) => setDeposit(Math.max(0, Number(event.target.value)))}
                      className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-lg font-semibold text-slate-900 outline-none transition focus:border-primary"
                    />
                  </div>
                  <p className="text-sm text-slate-600">{depositHint}</p>
                </div>
                <div className="mt-6 grid gap-4 sm:grid-cols-2">
                  <div className="rounded-[28px] bg-slate-50 p-4">
                    <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Pro capacity</p>
                    <p className="mt-3 text-3xl font-semibold text-slate-950">${estimatedCapacity}</p>
                  </div>
                  <div className="rounded-[28px] bg-slate-50 p-4">
                    <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Payable total</p>
                    <p className="mt-3 text-3xl font-semibold text-slate-950">${totalPayable}</p>
                  </div>
                </div>
                <div className="mt-6 rounded-[28px] border border-slate-200 bg-white p-4 text-sm leading-7 text-slate-700">
                  <p className="font-semibold text-slate-900">Fee structure</p>
                  <p className="mt-2">Fixed service fee: <span className="font-semibold text-slate-950">$35</span>. Pro Flasher unlocks measured flash capacity based on actual deposit amount and proven operator limits.</p>
                </div>
                <button className="mt-6 inline-flex h-14 w-full items-center justify-center rounded-full bg-primary px-6 text-sm font-semibold text-white transition hover:bg-slate-900">Pay $35 fee and continue</button>
              </div>
              <div className="space-y-4 rounded-[32px] border border-slate-200 bg-white p-5 shadow-sm">
                <h2 className="text-lg font-semibold text-slate-950">How it works</h2>
                <p className="text-sm leading-7 text-slate-600">Choose your deposit, pay a clear fixed fee, and begin a bridge session with real operator review. This helps avoid inflated estimates and keeps the flow grounded in the actual amount you fund.</p>
              </div>
            </div>
            <div className="space-y-5 rounded-[32px] border border-slate-200 bg-white p-6 shadow-sm">
              <div>
                <p className="text-sm uppercase tracking-[0.24em] text-primary">Price table</p>
                <div className="mt-4 space-y-4">
                  {priceTiers.map((tier) => (
                    <div key={tier.name} className="rounded-[24px] border border-slate-200 bg-slate-50 p-4">
                      <div className="flex items-center justify-between gap-3">
                        <p className="font-semibold text-slate-900">{tier.name}</p>
                        <p className="text-sm text-slate-500">{tier.fee}</p>
                      </div>
                      <p className="mt-2 text-sm text-slate-600">{tier.range}</p>
                    </div>
                  ))}
                </div>
              </div>
              <div className="rounded-[32px] border border-slate-200 bg-slate-50 p-5">
                <p className="text-sm uppercase tracking-[0.24em] text-primary">Explorer preview</p>
                <a
                  href="https://etherscan.io/tx/0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
                  target="_blank"
                  rel="noreferrer"
                  className="mt-3 inline-flex items-center gap-2 text-sm font-semibold text-primary"
                >
                  Transaction will appear here
                  <FiExternalLink />
                </a>
              </div>
              <div className="rounded-[32px] border border-slate-200 bg-white p-5 shadow-sm">
                <p className="text-sm font-semibold text-slate-900">Refund policy</p>
                <p className="mt-3 text-sm leading-7 text-slate-600">If your flash fails to settle within 20 minutes, you will receive a full refund within 24 hours.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

function HomePage() {
  const [openFeature, setOpenFeature] = useState(0);
  const [openFaq, setOpenFaq] = useState(0);
  const navigate = useNavigate();

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-6 sm:px-6 lg:px-8">
      <Helmet>
        <title>Silverback Flasher – Instant Cross-Chain Liquidity</title>
      </Helmet>
      <div className="mx-auto max-w-6xl space-y-10">
        <section className="rounded-[36px] border border-slate-200 bg-white/90 p-5 shadow-soft sm:p-8">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <span className="inline-flex rounded-full bg-primary/10 px-3 py-1 text-sm font-semibold text-primary">Silverback Flasher</span>
              <p className="mt-4 max-w-2xl text-base leading-8 text-slate-600 sm:text-lg">Enterprise flash liquidity for crypto teams. A polished bridge experience with clear wallet support, verified settlement, and operator monitoring.</p>
            </div>
            <div className="flex flex-wrap gap-2">
              {trustItems.map((item) => (
                <span key={item} className="inline-flex items-center rounded-full bg-slate-100 px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-slate-700 shadow-sm">{item}</span>
              ))}
            </div>
          </div>
        </section>

        <section className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="space-y-6 rounded-[40px] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
            <div className="space-y-4">
              <p className="text-sm uppercase tracking-[0.24em] text-primary">Flash liquidity bridge</p>
              <h1 className="text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">Flash liquidity across chains with instant, enterprise-grade precision.</h1>
              <p className="max-w-2xl text-base leading-8 text-slate-600 sm:text-lg">Built for BTC, ETH, LTC and USDT ERC-20 operators who need reliable, transparent settlement with a strong payment promise.</p>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <a href="https://t.me/SilverFlasher_bot" target="_blank" rel="noreferrer" className="inline-flex h-14 items-center justify-center rounded-full bg-primary text-sm font-semibold text-white transition hover:bg-slate-900">Chat with the Bridge Bot</a>
              <button type="button" onClick={() => navigate('/pro')} className="inline-flex h-14 items-center justify-center rounded-full border border-slate-300 bg-white text-sm font-semibold text-slate-900 transition hover:border-slate-400 hover:bg-slate-50">Bridge Now</button>
            </div>
            <div className="grid gap-4 sm:grid-cols-3">
              {metrics.map((metric) => (
                <div key={metric.label} className="rounded-[32px] border border-slate-200 bg-slate-50 p-5">
                  <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">{metric.label}</p>
                  <p className="mt-3 text-3xl font-semibold text-slate-950">{metric.value}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-[40px] border border-slate-200 bg-gradient-to-br from-primary/5 via-slate-50 to-white p-6 shadow-soft sm:p-8">
            <div className="space-y-4">
              <p className="text-sm uppercase tracking-[0.24em] text-primary">Trusted performance</p>
              <h2 className="text-3xl font-semibold tracking-tight text-slate-950">Pro Flasher plan built for trust.</h2>
              <p className="text-base leading-7 text-slate-600">Click Bridge Now to review pricing, capacity, refund guarantees and explorer visibility before you fund the session.</p>
            </div>
            <div className="mt-8 grid gap-4">
              <div className="rounded-[32px] bg-white px-5 py-6 shadow-sm">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Tier fee</p>
                    <p className="mt-2 text-lg font-semibold text-slate-950">Basic: $10 fee for $50-$500</p>
                  </div>
                  <FiShield className="text-primary" size={24} />
                </div>
              </div>
              <div className="rounded-[32px] bg-white px-5 py-6 shadow-sm">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Verification</p>
                    <p className="mt-2 text-lg font-semibold text-slate-950">Admin mark-as-paid workflow</p>
                  </div>
                  <FaCheckCircle className="text-emerald-500" size={24} />
                </div>
              </div>
              <div className="rounded-[32px] bg-white px-5 py-6 shadow-sm">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Refund</p>
                    <p className="mt-2 text-lg font-semibold text-slate-950">Full refund if not settled in 20 min</p>
                  </div>
                  <FiRefreshCcw className="text-secondary" size={24} />
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="space-y-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.24em] text-primary">Key benefits</p>
              <h2 className="mt-2 text-3xl font-semibold text-slate-950">Features built for modern flash liquidity.</h2>
            </div>
            <span className="rounded-full bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-700">Mobile-friendly & secure</span>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {features.map((feature, index) => (
              <FeatureItem key={feature.title} item={feature} isOpen={openFeature === index} onToggle={() => setOpenFeature(openFeature === index ? -1 : index)} />
            ))}
          </div>
        </section>

        <TestimonialsSection />

        <section className="space-y-6 rounded-[40px] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.24em] text-primary">Payment promise</p>
              <h2 className="text-3xl font-semibold text-slate-950">A dedicated promise page for every bridge.</h2>
            </div>
            <button type="button" onClick={() => navigate('/pro')} className="inline-flex h-14 items-center justify-center rounded-full bg-primary px-7 text-sm font-semibold text-white transition hover:bg-slate-900">Start the Pro Flasher</button>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-[32px] bg-slate-50 p-5">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Tier</p>
              <p className="mt-3 text-lg font-semibold text-slate-950">Basic</p>
              <p className="mt-2 text-sm text-slate-600">$50-500 bridge with a $10 fee.</p>
            </div>
            <div className="rounded-[32px] bg-slate-50 p-5">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Tier</p>
              <p className="mt-3 text-lg font-semibold text-slate-950">Pro Flasher</p>
              <p className="mt-2 text-sm text-slate-600">Start from a $35 service fee and unlock better bridge capacity.</p>
            </div>
            <div className="rounded-[32px] bg-slate-50 p-5">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Tier</p>
              <p className="mt-3 text-lg font-semibold text-slate-950">Enterprise</p>
              <p className="mt-2 text-sm text-slate-600">$10,000-50,000 bridge with premium operator support.</p>
            </div>
          </div>
        </section>

        <section className="space-y-6">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-primary">FAQ</p>
            <h2 className="mt-3 text-3xl font-semibold text-slate-950">Common questions answered.</h2>
          </div>
          <div className="grid gap-4">
            {faqs.map((faq, index) => (
              <FAQItem key={faq.question} faq={faq} isOpen={openFaq === index} onClick={() => setOpenFaq(openFaq === index ? -1 : index)} />
            ))}
          </div>
        </section>

        <footer className="rounded-[40px] border border-slate-200 bg-slate-950 p-6 text-slate-300 shadow-soft sm:p-8">
          <div className="grid gap-8 md:grid-cols-2">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-400">Contact</p>
              <p className="mt-4 text-base leading-7">Telegram: <a className="text-white underline" href="https://t.me/SilverFlasher_bot">@SilverFlasher_bot</a></p>
              <p className="mt-2 text-base leading-7">Email: <a className="text-white underline" href="mailto:support@hottboiihitzz.cc">support@hottboiihitzz.cc</a></p>
            </div>
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-400">Social</p>
              <div className="mt-4 flex flex-wrap gap-3">
                <a className="rounded-full border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800" href="#">Twitter</a>
                <a className="rounded-full border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800" href="#">LinkedIn</a>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </main>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/pro" element={<ProFlasherPage />} />
      </Routes>
    </Router>
  );
}
