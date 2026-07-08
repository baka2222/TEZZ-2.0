import React, { useEffect, useState } from 'react';
import axios from '../api/axios';
import { useParams, Link } from 'react-router-dom';
import { Calendar, Clock, Edit3 } from 'lucide-react';

export default function LessonPage() {
  const { moduleId, lessonId } = useParams();
  const [lesson, setLesson] = useState(null);
  const [user, setUser] = useState(null);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [updateStatus, setUpdateStatus] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError('');
        
        const [lessonRes, userRes] = await Promise.all([
          axios.get(`/lessons/${lessonId}/`),
          axios.get('/profile/')
        ]);

        setLesson(lessonRes.data);
        setUser(userRes.data);

        if (userRes.data.role === 'teacher') {
          const studentsRes = await axios.get(`/lessons/${lessonId}/students/`);
          setStudents(studentsRes.data);
        } else {
          try {
            const marksRes = await axios.get(`/marks/${lessonId}/`);
            setStudents(marksRes.data);
          } catch (err) {
            // Если оценок нет, устанавливаем пустой массив
            setStudents([]);
          }
        }
      } catch (err) {
        console.error('Ошибка загрузки урока:', err);
        setError('Не удалось загрузить урок');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [lessonId]);

// ---------- handleScoreUpdate ----------
const handleScoreUpdate = async (markId, newScore, studentId) => {
  console.log('handleScoreUpdate', { markId, newScore, studentId });

  if (!markId) {
    setUpdateStatus('Сначала создайте запись оценки (mark) в админке или пересохраните урок');
    setTimeout(() => setUpdateStatus(''), 4000);
    return;
  }

  const payload = { score: newScore === '' ? null : Number(newScore) };
  try {
    await axios.patch(`/marks/${markId}/update/`, payload);
    // обновляем локально: у teacher-view students приходят как User с полем 'mark' и 'mark_id'
    setStudents(prev => prev.map(s => (s.mark_id === markId ? { ...s, mark: payload.score } : s)));
    setUpdateStatus('Оценка обновлена');
    setTimeout(() => setUpdateStatus(''), 3000);
  } catch (err) {
    console.error('Ошибка обновления оценки:', err);
    setUpdateStatus('Ошибка обновления оценки');
    setTimeout(() => setUpdateStatus(''), 4000);
  }
};

const handleFileUpload = async () => {
  if (!file) return;
  
  try {
    setUploading(true);
    
    // Проверяем, есть ли у студента уже оценка
    console.log(students);
    let markId = null;
    if (students.length > 0 && students[0].id) {
      markId = students[0].id;
    }
    
    if (!markId) {
      setUpdateStatus('Сначала учитель должен создать оценку');
      return;
    }
    
    const formData = new FormData();
    formData.append('answer', file);
    
    const res = await axios.patch(`/marks/${markId}/update/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    setUpdateStatus('Файл успешно загружен');
    setTimeout(() => setUpdateStatus(''), 3000);
    setFile(null);
  } catch (err) {
    console.error('Ошибка загрузки файла:', err);
    setUpdateStatus('Ошибка загрузки файла');
  } finally {
    setUploading(false);
  }
};



  // Функция для форматирования даты и времени
  function formatDateTime (iso, { month = true, year = false, tz = null } = {}) {
  if (!iso) return 'Не указано';
  const d = new Date(iso);
  if (isNaN(d)) return 'Не указано';

  const dateOpts = { day: 'numeric' };
  if (month) dateOpts.month = 'long';
  if (month && year) dateOpts.year = 'numeric';
  if (tz) dateOpts.timeZone = tz;

  const timeOpts = { hour: '2-digit', minute: '2-digit' };
  if (tz) timeOpts.timeZone = tz;

  return `${new Intl.DateTimeFormat('ru-RU', dateOpts).format(d)}, ${new Intl.DateTimeFormat('ru-RU', timeOpts).format(d)}`;
}

  if (loading) {
    return (
      <div className="lesson-loading">
        <div className="loading-spinner"></div>
        <p>Загрузка урока...</p>
      </div>
    );
  }

  if (error || !lesson) {
    return (
      <div className="lesson-error">
        <h2>Ошибка</h2>
        <p>{error || 'Урок не найден'}</p>
        <Link to={`/modules/${moduleId}`} className="back-link">
          ← Назад к модулю
        </Link>
      </div>
    );
  }

  return (
    <div className="lesson-container">
      <div className="lesson-header">
        <Link to={`/modules/${moduleId}`} className="back-link">
          ← Назад к модулю
        </Link>
        <h1 className="lesson-title">{lesson.title}</h1>
        
        <div className="lesson-meta">
          <div className="meta-item">
            <Calendar size={16} />
            <span>Создан: {formatDateTime(lesson.created_at)}</span>
          </div>
          <div className="meta-item">
            <Edit3 size={16} />
            <span>Обновлен: {formatDateTime(lesson.updated_at)}</span>
          </div>
          {lesson.start_time && (
            <div className="meta-item">
              <Clock size={16} />
              <span>Начало урока: {formatDateTime(lesson.start_time)}</span>
            </div>
          )}
          {lesson.end_time && (
            <div className="meta-item">
              <Clock size={16} />
              <span>Окончание урока: {formatDateTime(lesson.end_time)}</span>
            </div>
          )}
        </div>
        
        {lesson.description && (
          <p className="lesson-description">{lesson.description}</p>
        )}
        {lesson.content && (
          <div className="lesson-content">
            <h3>Домашняя работа:</h3>
             <div className="hw-text" style={{ whiteSpace: 'pre-wrap' }}>
              {lesson.content}
            </div>
          </div>
        )}
      </div>

      {updateStatus && (
        <div className={`update-status ${updateStatus.includes('Ошибка') ? 'error' : 'success'}`}>
          {updateStatus}
        </div>
      )}

      <div className="lesson-main-content">
        {user?.role === 'teacher' ? (
          <div className="teacher-view">
            <h2 className="section-title">Студенты и оценки</h2>
            
            {students.length > 0 ? (
              <div className="students-table">
                <div className="table-header">
                  <div className="table-cell">Студент</div>
                  <div className="table-cell">Оценка</div>
                  <div className="table-cell">Действия</div>
                  <div className="table-cell">Работа</div>
                </div>
                
                {students.map(student => (
                  console.log(student),
                  <div key={student.id} className="table-row">
                    <div className="table-cell">
                      {student.first_name || `Студент #${student.id}`}
                    </div>
                    <div className="table-cell">
                      <span className={`score ${student.mark !== null && student.score !== undefined ? 'has-score' : 'no-score'}`}>
  {student.mark !== null && student.mark !== undefined ? student.mark : '—'}
</span>
                    </div>
                    <div className="table-cell">
                      <input
                        type="text"
                        inputMode="numeric"
                        pattern="\d*"
                        value={ (student.mark ?? student.score) ?? '' } // кросс-совместимость: поддержит и 'mark' и 'score'
                        onChange={(e) => {
                          const v = e.target.value.replace(/\D+/g, ''); // только цифры
                          setStudents(prev => prev.map(s => s.id === student.id ? { ...s, mark: v, score: v } : s));
                        }}
                        className="score-input"
                        placeholder="0-100"
                        style={{ width: 90 }}
                      />

                      <button
                        onClick={() => handleScoreUpdate(student.mark_id, (student.mark ?? student.score) ?? '', student.id)}
                        className="update-score-btn"
                        style={{ marginLeft: 8, padding: '6px 12px' }}
                        disabled={!student.mark_id}
                        title={!student.mark_id ? 'Нет записи оценки (mark). Создайте через админку или пересохраните урок.' : 'Сохранить оценку'}
                      >
                        {student.mark_id ? 'Обновить' : 'Нет mark'}
                      </button>
                    </div>
                    <div className="table-cell">
                      <a 
                        href={student.answer_url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                      >
                        Посмотреть работу
                      </a>

                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-students">
                <p>На этот урок еще не записаны студенты</p>
              </div>
            )}
          </div>
        ) : (
          <div className="student-view">
            <h2 className="section-title">Ваша работа</h2>
            
            {students.length > 0 && students[0].score ? (
              <div className="score-display">
                <h3>Ваша оценка</h3>
                <span className="score-value">{students[0].score}</span>
                <span className="score-label">баллов</span>
              </div>
            ) : (
              <div className="no-score">
                <p>Оценка еще не выставлена</p>
              </div>
            )}
            
            <div className="file-upload-section">
              <h3>Загрузить ответ</h3>
              <div className="file-upload">
                <input
                  type="file"
                  id="file-upload"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="file-input"
                />
                <label htmlFor="file-upload" className="file-label">
                  {file ? file.name : 'Выберите файл'}
                </label>
                <button
                  onClick={handleFileUpload}
                  disabled={!file || uploading}
                  className="upload-button"
                >
                  {uploading ? 'Загрузка...' : 'Загрузить'}
                </button>
              </div>
              <p className="file-help">Загрузите файл с вашим ответом на задание</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}