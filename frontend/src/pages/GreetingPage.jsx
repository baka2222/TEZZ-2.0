import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

export default function LandingPage() {
  const navigate = useNavigate();
  const [isVisible, setIsVisible] = useState({});
  
  const sectionRefs = {
    hero: useRef(null),
    courses: useRef(null),
    benefits: useRef(null),
    cta: useRef(null)
  };

  const courseRefs = useRef([]);
  const benefitRefs = useRef([]);

  useEffect(() => {
    const observers = [];
    
    // Observer для всех секций
    Object.keys(sectionRefs).forEach(key => {
      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            setIsVisible(prev => ({ ...prev, [key]: true }));
          }
        },
        { 
          threshold: 0.1,
          rootMargin: '0px 0px -50px 0px'
        }
      );
      
      if (sectionRefs[key].current) {
        observer.observe(sectionRefs[key].current);
        observers.push(observer);
      }
    });

    // Observer для отдельных карточек курсов
    const courseObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('landing-course-visible');
          }
        });
      },
      { 
        threshold: 0.1,
        rootMargin: '0px 0px -30px 0px'
      }
    );

    // Observer для преимуществ
    const benefitObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('landing-benefit-visible');
          }
        });
      },
      { 
        threshold: 0.1,
        rootMargin: '0px 0px -30px 0px'
      }
    );

    // Наблюдаем за карточками курсов
    courseRefs.current.forEach(card => {
      if (card) courseObserver.observe(card);
    });

    // Наблюдаем за преимуществами
    benefitRefs.current.forEach(benefit => {
      if (benefit) benefitObserver.observe(benefit);
    });

    return () => {
      observers.forEach(observer => observer.disconnect());
      courseObserver.disconnect();
      benefitObserver.disconnect();
    };
  }, []);

  const handleNavigateToLogin = () => {
    navigate('/login');
  };

  const courses = [
    {
      icon: '💻',
      title: 'Программирование',
      description: 'Python, JavaScript, C++ и современные фреймворки'
    },
    {
      icon: '🤖',
      title: 'Робототехника',
      description: 'Arduino, Raspberry Pi и IoT устройства'
    },
    {
      icon: '⚡',
      title: 'Физика',
      description: 'Эксперименты и исследование законов вселенной'
    },
    {
      icon: '📊',
      title: 'Математика',
      description: 'Алгебра, геометрия и математический анализ'
    }
  ];

  const benefits = [
    {
      icon: '🚀',
      title: 'Практические проекты',
      description: 'Реальные кейсы и проектная работа'
    },
    {
      icon: '👨‍🏫',
      title: 'Эксперты индустрии',
      description: 'Преподаватели с опытом в IT и engineering'
    },
    {
      icon: '🏆',
      title: 'Подготовка к олимпиадам',
      description: 'Успешное выступление на конкурсах'
    },
    {
      icon: '💡',
      title: 'Инновации',
      description: 'Современные технологии и методики'
    }
  ];

  // Функции для добавления refs
  const addCourseRef = (el, index) => {
    courseRefs.current[index] = el;
  };

  const addBenefitRef = (el, index) => {
    benefitRefs.current[index] = el;
  };

  return (
    <div className="landing-container">
      <Helmet>
        <title>STEM курсы в Бишкеке — Программирование, ОРТ и робототехника</title>
        <meta
          name="description"
          content="Онлайн и оффлайн курсы по программированию, робототехнике и школьной физике и математике"
        />
        <meta property="og:title" content="TEZZ - STEM курсы в Бишкеке" />
        <meta property="og:description" content="Онлайн и оффлайн курсы по программированию, робототехнике и школьной физике и математике" />
        <meta property="og:url" content="https://tezz.kg/greeting" />
        <meta property="og:type" content="website" />
      </Helmet>
      {/* Анимированный фон */}
      <div className="landing-background">
        <div className="landing-bg-glow-1"></div>
        <div className="landing-bg-glow-2"></div>
        <div className="landing-bg-glow-3"></div>
      </div>

      {/* Хедер */}
      <header className="landing-header">
        <div className="landing-header-content">
          <div className="landing-logo-section">
            <div className="landing-tezz-logo-large">TEZZ STEM</div>
            <div className="landing-logo-subtitle">Образовательный центр</div>
          </div>
          <button className="landing-login-btn" onClick={handleNavigateToLogin}>
            Войти
          </button>
        </div>
      </header>

      {/* Герой секция */}
      <section 
        ref={sectionRefs.hero}
        className={`landing-hero-section ${isVisible.hero ? 'landing-visible' : ''}`}
      >
        <div className="landing-hero-content">
          <div className="landing-hero-badge">
            <span>🎯 Будущее начинается здесь</span>
          </div>
          <h1 className="landing-hero-title">
            STEM-образование
            <span className="landing-gradient-text"> нового поколения</span>
          </h1>
          <p className="landing-hero-description">
            Программирование, робототехника, физика и математика для детей и подростков. 
            Практические навыки, которые помогут построить успешное будущее в мире технологий.
          </p>
          <div className="landing-hero-actions">
            <button className="landing-cta-button landing-primary" onClick={() => window.open('https://t.me/isbakks', '_blank')}>
              Начать обучение
            </button>
            <button
              className="landing-cta-button landing-secondary"
              onClick={() => window.open('https://www.instagram.com/tezz_edu?igsh=Y3ZuejIyZ296MHc5&utm_source=qr', '_blank')}
            >
              Узнать больше
            </button>
          </div>
        </div>
        
        <div className="landing-hero-visual">
          <div className="landing-floating-cards">
            <div className="landing-floating-card landing-card-1">💻</div>
            <div className="landing-floating-card landing-card-2">🤖</div>
            <div className="landing-floating-card landing-card-3">⚡</div>
            <div className="landing-floating-card landing-card-4">📊</div>
          </div>
        </div>
      </section>

      {/* Секция курсов */}
      <section 
        ref={sectionRefs.courses}
        className={`landing-courses-section ${isVisible.courses ? 'landing-visible' : ''}`}
      >
        <div className="landing-section-header">
          <h2>Направления обучения</h2>
          <p>Комплексный подход к STEM-образованию</p>
        </div>
        
        <div className="landing-courses-grid">
          {courses.map((course, index) => (
            <div 
              key={index} 
              ref={el => addCourseRef(el, index)}
              className="landing-course-card"
            >
              <div className="landing-course-icon">{course.icon}</div>
              <h3>{course.title}</h3>
              <p>{course.description}</p>
              <div className="landing-course-features">
                <span className="landing-feature-tag">✓ Проекты</span>
                <span className="landing-feature-tag">✓ Практика</span>
                <span className="landing-feature-tag">✓ Поддержка</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Секция преимуществ */}
      <section 
        ref={sectionRefs.benefits}
        className={`landing-benefits-section ${isVisible.benefits ? 'landing-visible' : ''}`}
      >
        <div className="landing-benefits-content">
          <div className="landing-benefits-text">
            <div className="landing-section-header landing-text-left">
              <h2>Почему выбирают TEZZ STEM?</h2>
              <p>Наши преимущества для успешного обучения</p>
            </div>
            <div className="landing-benefits-list">
              {benefits.map((benefit, index) => (
                <div 
                  key={index} 
                  ref={el => addBenefitRef(el, index)}
                  className="landing-benefit-item"
                >
                  <div className="landing-benefit-icon">{benefit.icon}</div>
                  <div>
                    <h4>{benefit.title}</h4>
                    <p>{benefit.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA секция */}
      <section 
        ref={sectionRefs.cta}
        className={`landing-cta-section ${isVisible.cta ? 'landing-visible' : ''}`}
      >
        <div className="landing-cta-card">
          <h2>Готовы начать обучение?</h2>
          <p>Присоединяйтесь к TEZZ STEM и откройте мир технологий</p>
          <button className="landing-cta-button landing-primary landing-large" onClick={() => window.open('https://t.me/isbakks', '_blank')}>
            Записаться на курс
          </button>
        </div>
      </section>

      {/* Футер */}
      <footer className="landing-footer">
        <div className="landing-footer-content">
          <div className="landing-footer-section">
            <div className="landing-tezz-logo">TEZZ STEM</div>
            <p>Образовательный центр будущего</p>
          </div>
          <div className="landing-footer-section">
            <h4>Контакты</h4>
            <button className="landing-telegram-link">
              <a href='https://t.me/isbakks'>Telegram: @isbakks</a>
            </button>
            <p>email: ikaoss222@gmail.com</p>
          </div>
        </div>
        <div className="landing-footer-bottom">
          <p>© 2024 TEZZ STEM. Все права защищены.</p>
        </div>
      </footer>
    </div>
  );
}