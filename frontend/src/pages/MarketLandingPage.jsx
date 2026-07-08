import React, { useEffect, useRef, useState } from "react";
import { Helmet } from "react-helmet-async";
import logo from '../assets/tezz_logo.png'

export default function TezzMarketLanding() {
  const [isVisible, setIsVisible] = useState({});

  // Рефы для секций
  const sectionRefs = {
    hero: useRef(null),
    how: useRef(null),
    features: useRef(null),
    examples: useRef(null),
    cta: useRef(null),
  };

  // Рефы для карточек (чтобы анимировать их по отдельности)
  const featureRefs = useRef([]);
  const exampleRefs = useRef([]);

  useEffect(() => {
    const observers = [];

    // Наблюдатель для секций
    Object.keys(sectionRefs).forEach((key) => {
      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            setIsVisible((prev) => ({ ...prev, [key]: true }));
          }
        },
        { threshold: 0.1, rootMargin: "0px 0px -50px 0px" }
      );
      if (sectionRefs[key].current) {
        observer.observe(sectionRefs[key].current);
        observers.push(observer);
      }
    });

    // Наблюдатель для карточек преимуществ
    const featureObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("feature-visible");
          }
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -30px 0px" }
    );

    featureRefs.current.forEach((el) => {
      if (el) featureObserver.observe(el);
    });

    // Наблюдатель для карточек примеров
    const exampleObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("example-visible");
          }
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -30px 0px" }
    );

    exampleRefs.current.forEach((el) => {
      if (el) exampleObserver.observe(el);
    });

    return () => {
      observers.forEach((obs) => obs.disconnect());
      featureObserver.disconnect();
      exampleObserver.disconnect();
    };
  }, []);

  // Вспомогательные функции для заполнения массивов рефов
  const addFeatureRef = (el, index) => {
    featureRefs.current[index] = el;
  };
  const addExampleRef = (el, index) => {
    exampleRefs.current[index] = el;
  };

  return (
    <div className="tezz-root">
      {/* SEO-метаданные */}
      <Helmet>
        <title>TEZZ MARKET — покупка и продажа в Telegram | Веломаркет, техника</title>
        <meta
          name="description"
          content="Объявления из Telegram‑каналов, покупка через бота @tez4917_bot. Веломаркет (2000+ подписчиков), техника, услуги мастерских. Всё бесплатно."
        />
        <meta property="og:title" content="TEZZ MARKET — покупка в Telegram" />
        <meta
          property="og:description"
          content="Покупайте велосипеды, технику и услуги прямо в Telegram. Быстро, бесплатно, надёжно."
        />
        <meta property="og:url" content="https://t.me/tez4917_bot" />
        <meta property="og:type" content="website" />
      </Helmet>

      {/* Шапка (без анимации) */}
      <header className="tm-header">
        <div className="tm-container tm-header-inner">
          <div className="tm-brand">
            <img src={logo} alt="TEZZ Logo" className="tm-logo" />
            <div>
              <h1 className="tm-title">TEZZ MARKET</h1>
              <p className="tm-tag">Объявления из Telegram‑каналов • Покупка в один клик</p>
            </div>
          </div>

          <nav className="tm-nav">
            <a href="#how">Как работает</a>
            <a className="tm-cta" href="https://t.me/tez4917_bot" target="_blank" rel="noopener noreferrer">Перейти в бот</a>
          </nav>
        </div>
      </header>

      <main>
        {/* Герой-секция */}
        <section
          ref={sectionRefs.hero}
          className={`tm-hero ${isVisible.hero ? "fade-in" : ""}`}
        >
          <div className="tm-container tm-hero-grid">
            <div className="tm-hero-left">
              <h2 className="hero-h1">Покупайте и продавайте<br />прямо в Telegram</h2>
              <p className="hero-lead">
                Бот @tez4917_bot связан с тематическими каналами — вы видите объявления,
                переходите по кнопке и совершаете сделку. Доставка, запись в мастерские,
                быстрые платежи — всё внутри бота.
              </p>

              <div className="hero-actions">
                <a className="btn-primary" href="https://t.me/tez4917_bot" target="_blank" rel="noopener noreferrer">Начать покупать</a>
                <a className="btn-ghost" href="#how">Как это работает</a>
              </div>

              <ul className="tm-bullets">
                <li>✅ 2000+ подписчиков в веломаркете — реальные предложения</li>
                <li>✅ Совершенно бесплатно (опциональные интервалы для повторов)</li>
                <li>✅ Техника, велосипеды, запчасти и услуги мастерских</li>
              </ul>
            </div>

            <aside className="tm-hero-right">
              <div className="preview-card">
                <div className="preview-tag">🔥 Свежее в веломаркете</div>
                <h3>Велосипед Author Traction 2022</h3>
                <p className="muted">Рама L • дисковые тормоза • отличное состояние</p>
                <div className="preview-meta">
                  <span>💰 45 000 ₽</span>
                  <span>📍 Ташкент</span>
                </div>
                <div className="preview-actions">
                  <a className="btn-small" href="https://t.me/tez4917_bot" target="_blank" rel="noopener noreferrer">Связаться</a>
                  <a className="btn-small outline" href="https://t.me/tez4917_bot" target="_blank" rel="noopener noreferrer">Забронировать</a>
                </div>
              </div>

              <div className="trust">
                <strong>⚡ Мгновенные сделки</strong>
                <p className="muted">Переходите в бот, договаривайтесь и оплачивайте — всё в одном месте.</p>
              </div>
            </aside>
          </div>
        </section>

        {/* Как работает */}
        <section
          id="how"
          ref={sectionRefs.how}
          className={`tm-section tm-how ${isVisible.how ? "slide-up" : ""}`}
        >
          <div className="tm-container">
            <h3 className="section-title">Как это работает</h3>
            <div className="how-grid">
              <div className="how-step">
                <div className="step-ico">📢</div>
                <h4>1. Смотрите каналы</h4>
                <p>Объявления публикуются в тематических каналах (вело, техника, услуги).</p>
              </div>
              <div className="how-step">
                <div className="step-ico">🤖</div>
                <h4>2. Переходите в бот</h4>
                <p>Нажимаете «Связаться» под объявлением — открывается диалог с @tez4917_bot.</p>
              </div>
              <div className="how-step">
                <div className="step-ico">🛒</div>
                <h4>3. Покупаете или записываетесь</h4>
                <p>Оплата, доставка, запись в веломастерскую — бот проводит сделку.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Преимущества (с отдельными анимациями для карточек) */}
        <section
          id="features"
          ref={sectionRefs.features}
          className={`tm-section tm-features ${isVisible.features ? "fade-in" : ""}`}
        >
          <div className="tm-container">
            <h3 className="section-title">Почему выбирают TezzMarket</h3>
            <div className="features-grid">
              <Feature
                ref={(el) => addFeatureRef(el, 0)}
                title="Полностью бесплатно"
                desc="Никаких комиссий за покупку или размещение. Можно оплатить только ускоренный повтор объявления."
              />
              <Feature
                ref={(el) => addFeatureRef(el, 1)}
                title="Доставка через бота"
                desc="Оформляйте доставку прямо в Telegram, без лишних приложений."
              />
              <Feature
                ref={(el) => addFeatureRef(el, 2)}
                title="Запись в мастерские"
                desc="Ремонт велосипедов, обслуживание техники — выбирайте время и мастера."
              />
              <Feature
                ref={(el) => addFeatureRef(el, 3)}
                title="Проверенные продавцы"
                desc="В каналах только реальные объявления, модерация исключает мошенников."
              />
            </div>
          </div>
        </section>

        {/* Примеры объявлений (с отдельными анимациями) */}
        <section
          id="examples"
          ref={sectionRefs.examples}
          className={`tm-section tm-examples ${isVisible.examples ? "fade-in" : ""}`}
        >
          <div className="tm-container">
            <h3 className="section-title">Свежие предложения</h3>
            <div className="examples-grid">
              <ListingCard
                ref={(el) => addExampleRef(el, 0)}
                title="Горный велосипед Merida Big Nine"
                description='Рама 19", алюминий, 24 скорости, гидравлика'
                price="52 000 ₽"
                location="Ташкент"
              />
              <ListingCard
                ref={(el) => addExampleRef(el, 1)}
                title="iPhone 13 Pro 256GB"
                description="Графитовый, комплект, чехол, стекло"
                price="680 000 ₽"
                location="Бишкек"
              />
              <ListingCard
                ref={(el) => addExampleRef(el, 2)}
                title="Запись в веломастерскую"
                description="Регулировка тормозов, замена кассеты"
                price="от 15 000 ₽"
                location="Любой район"
              />
            </div>
          </div>
        </section>

        {/* Призыв к действию */}
        <section
          ref={sectionRefs.cta}
          className={`tm-cta-section ${isVisible.cta ? "scale-in" : ""}`}
        >
          <div className="tm-container tm-cta-block">
            <div>
              <h3 className="cta-h">Уже более <span className="accent">2000 человек</span> покупают через TezzMarket</h3>
              <p className="muted">Присоединяйтесь — просто откройте бота и выберите товар.</p>
            </div>
            <div className="cta-actions">
              <a className="btn-primary large" href="https://t.me/tez4917_bot" target="_blank" rel="noopener noreferrer">🚀 Перейти в бот</a>
              <a className="btn-ghost" href="#">Как оформить доставку</a>
            </div>
          </div>
        </section>
      </main>

      <footer className="tm-footer">
        <div className="tm-container tm-footer-inner">
          <div>© {new Date().getFullYear()} TEZZ MARKET — бот: <a href="https://t.me/tez4917_bot" target="_blank" rel="noopener noreferrer">@tez4917_bot</a></div>
          <div className="muted">Работает в Telegram • Все категории</div>
        </div>
      </footer>

      {/* Обновлённые стили с анимациями */}
      <style>{`
        :root{ --tm-green: #2f6b3a; --tm-brown: #3d2f24; --tm-cream: #fbf6e6; --tm-muted:#6b6b6b; }
        .tezz-root{ font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; color: var(--tm-brown); background: var(--tm-cream); min-height:100vh; }
        .tm-container{ max-width:1100px; margin:0 auto; padding:28px; }

        /* Header (без анимации) */
        .tm-header{ border-bottom: 1px solid rgba(0,0,0,0.06); background: linear-gradient(90deg, rgba(255,255,255,0.6), rgba(255,255,255,0.9)); position:sticky; top:0; z-index:40; backdrop-filter: blur(4px); }
        .tm-header-inner{ display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; }
        .tm-brand{ display:flex; gap:12px; align-items:center; }
        .tm-logo{ width:64px; height:64px; flex:0 0 64px; object-fit: contain; }
        .tm-title{ margin:0; font-size:18px; letter-spacing:1px; color:var(--tm-brown); }
        .tm-tag{ margin:0; font-size:12px; color:var(--tm-muted); }
        .tm-nav{ display:flex; flex-wrap:wrap; align-items:center; }
        .tm-nav a{ margin-left:18px; text-decoration:none; color:var(--tm-brown); font-weight:600; transition: opacity 0.2s; }
        .tm-nav a:hover{ opacity:0.7; }
        .tm-nav a.tm-cta { 
          background: var(--tm-brown); 
          color: #ffffff !important; /* Форсируем белый */
          padding: 10px 14px; 
          border-radius: 8px; 
          text-decoration: none; 
          font-weight: 600; 
        }

        /* Hero */
        .tm-hero{ padding:48px 0; opacity:0; transform:translateY(20px); transition: opacity 0.8s ease, transform 0.8s ease; }
        .tm-hero.fade-in{ opacity:1; transform:translateY(0); }
        .tm-hero-grid{ display:grid; grid-template-columns: 1fr 360px; gap:28px; align-items:start; }
        .hero-h1{ font-size:34px; margin:0 0 12px; line-height:1.05; color:var(--tm-brown); }
        .hero-lead{ color:var(--tm-muted); margin:0 0 18px; font-size:1.1rem; }
        .hero-actions{ display:flex; gap:12px; margin-bottom:18px; flex-wrap:wrap; }
        .btn-primary{ background:var(--tm-green); color:var(--tm-cream); padding:12px 16px; border-radius:10px; text-decoration:none; font-weight:700; box-shadow:0 4px 8px rgba(47,107,58,0.2); transition: background 0.2s; }
        .btn-primary:hover{ background:#1f4f2a; }
        .btn-ghost{ background:transparent; border:1px solid rgba(0,0,0,0.06); padding:12px 16px; border-radius:10px; text-decoration:none; color:var(--tm-brown); transition: background 0.2s; }
        .btn-ghost:hover{ background:rgba(0,0,0,0.02); }
        .tm-bullets{ margin:12px 0 0; list-style:none; padding:0; color:var(--tm-muted); }
        .tm-bullets li{ margin-bottom:8px; display:flex; align-items:center; gap:6px; }

        .preview-card{ background: white; border-radius:12px; padding:16px; box-shadow:0 8px 20px rgba(45,45,45,0.06); transition: transform 0.2s; }
        .preview-card:hover{ transform:translateY(-2px); }
        .preview-tag{ display:inline-block; background:var(--tm-cream); padding:6px 8px; border-radius:6px; font-size:12px; margin-bottom:6px; color:var(--tm-brown); font-weight:600; }
        .preview-card h3{ margin:6px 0; }
        .preview-meta{ font-size:12px; color:var(--tm-muted); display:flex; justify-content:space-between; margin-top:8px; }
        .preview-actions{ display:flex; gap:8px; margin-top:12px; }
        .btn-small{ padding:8px 10px; border-radius:8px; background:var(--tm-green); color:var(--tm-cream); text-decoration:none; font-weight:600; font-size:13px; transition: background 0.2s; }
        .btn-small:hover{ background:#1f4f2a; }
        .btn-small.outline{ background:transparent; border:1px solid rgba(0,0,0,0.06); color:var(--tm-brown); }
        .btn-small.outline:hover{ background:rgba(0,0,0,0.02); }

        .trust{ margin-top:18px; background:linear-gradient(180deg, rgba(47,107,58,0.06), transparent); border-radius:10px; padding:10px; }

        /* Секции */
        .tm-section{ padding:36px 0; }
        .section-title{ font-size:26px; margin-bottom:24px; color:var(--tm-brown); position:relative; display:inline-block; }
        .section-title:after{ content:''; position:absolute; bottom:-6px; left:0; width:60px; height:3px; background:var(--tm-green); border-radius:2px; }

        /* Анимации для секций */
        .tm-how, .tm-features, .tm-examples, .tm-cta-section {
          opacity:0; transform:translateY(20px); transition: opacity 0.8s ease, transform 0.8s ease;
        }
        .tm-how.slide-up, .tm-features.fade-in, .tm-examples.fade-in, .tm-cta-section.scale-in {
          opacity:1; transform:translateY(0);
        }
        .tm-cta-section.scale-in { transform:scale(1); }

        /* Сетки */
        .how-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }
        .how-step{ background:white; border-radius:10px; padding:16px; box-shadow:0 6px 18px rgba(0,0,0,0.04); transition: box-shadow 0.2s; }
        .how-step:hover{ box-shadow:0 8px 24px rgba(0,0,0,0.08); }
        .step-ico{ width:42px; height:42px; border-radius:10px; background:var(--tm-green); color:var(--tm-cream); display:flex; align-items:center; justify-content:center; font-weight:700; margin-bottom:10px; }

        .features-grid{ display:grid; grid-template-columns:repeat(2,1fr); gap:18px; }
        .feature-card { background:white; border-radius:10px; padding:16px; box-shadow:0 6px 18px rgba(0,0,0,0.04); transition: opacity 0.6s ease, transform 0.6s ease; opacity:0; transform:translateY(20px); }
        .feature-card.feature-visible { opacity:1; transform:translateY(0); }

        .examples-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
        .listing{ background:white; padding:16px; border-radius:10px; box-shadow:0 6px 14px rgba(0,0,0,0.04); transition: opacity 0.6s ease, transform 0.6s ease; opacity:0; transform:translateY(20px); }
        .listing.example-visible { opacity:1; transform:translateY(0); }
        .listing:hover{ transform:translateY(-2px); }
        .listing h4{ margin:6px 0; }
        .listing .price{ font-weight:700; color:var(--tm-green); }
        .muted{ color:var(--tm-muted); }

        /* CTA */
        .tm-cta-section{ background:linear-gradient(90deg, rgba(47,107,58,0.06), rgba(61,47,36,0.02)); padding:28px 0; border-top:1px solid rgba(0,0,0,0.03); }
        .tm-cta-block{ display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; }
        .cta-h{ margin:0; font-size:24px; }
        .accent{ color:var(--tm-green); font-weight:800; }
        .cta-actions{ display:flex; gap:12px; flex-wrap:wrap; }
        .btn-primary.large{ padding:14px 20px; font-size:16px; }

        /* Footer */  
        .tm-footer{ padding:18px 0; color:var(--tm-muted); border-top:1px solid rgba(0,0,0,0.04); }
        .tm-footer-inner{ display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap; }

        /* Responsive */
        @media (max-width:980px){
          .tm-hero-grid{ grid-template-columns:1fr; }
          .how-grid{ grid-template-columns:1fr; }
          .features-grid{ grid-template-columns:1fr; }
          .examples-grid{ grid-template-columns:1fr; }
          .tm-cta-block{ flex-direction:column; align-items:flex-start; }
          .tm-header-inner{ flex-direction:column; align-items:flex-start; }
          .tm-nav{ margin-top:10px; }
          .tm-nav a{ margin-left:0; margin-right:18px; }
        }
      `}</style>
    </div>
  );
}

// Компонент Feature с поддержкой ref
const Feature = React.forwardRef(({ title, desc }, ref) => {
  return (
    <div ref={ref} className="feature-card">
      <div className="step-ico">✓</div>
      <h4>{title}</h4>
      <p className="muted">{desc}</p>
    </div>
  );
});

// Компонент ListingCard с поддержкой ref
const ListingCard = React.forwardRef(({ title, description, price, location }, ref) => {
  return (
    <div ref={ref} className="listing">
      <h4>{title}</h4>
      <p className="muted" style={{ margin: '4px 0' }}>{description}</p>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', margin: '10px 0' }}>
        <span className="price">{price}</span>
        <span className="muted">{location}</span>
      </div>
      <div className="preview-actions">
        <a className="btn-small" href="https://t.me/tez4917_bot" target="_blank" rel="noopener noreferrer">Купить</a>
        <a className="btn-small outline" href="https://t.me/tez4917_bot" target="_blank" rel="noopener noreferrer">Подробнее</a>
      </div>
    </div>
  );
});