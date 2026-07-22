import LessonView from "@/components/views/LessonView";

export default async function LessonPage({
  params,
}: {
  params: Promise<{ moduleId: string; lessonId: string }>;
}) {
  const { moduleId, lessonId } = await params;
  return <LessonView moduleId={moduleId} lessonId={lessonId} />;
}
