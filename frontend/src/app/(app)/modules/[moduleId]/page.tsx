import ModuleView from "@/components/views/ModuleView";

export default async function ModulePage({
  params,
}: {
  params: Promise<{ moduleId: string }>;
}) {
  const { moduleId } = await params;
  return <ModuleView moduleId={moduleId} />;
}
