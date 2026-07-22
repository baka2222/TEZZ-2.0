export interface Profile {
  id: number;
  first_name: string;
  telegram?: string | null;
  discord?: string | null;
  role?: "teacher" | "student" | string;
}

export interface Lesson {
  id: number;
  title: string;
  content?: string | null;
  description?: string | null;
  start_time?: string | null;
  end_time?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
  student_mark?: number | null;
}

export interface Module {
  id: number;
  title: string;
  description?: string | null;
  lessons: Lesson[];
}

/** Строка в списке студентов/оценок урока (teacher- и student-view). */
export interface MarkRow {
  id: number;
  first_name?: string | null;
  mark?: number | null;
  score?: number | null;
  mark_id?: number | null;
  answer_url?: string | null;
}
