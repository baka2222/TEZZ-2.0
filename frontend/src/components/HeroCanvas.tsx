"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";

/**
 * Интерактивная 3D-сцена героя (перенос из импортированного дизайна):
 * глянцевый торический узел бренда + кремовая wireframe-оболочка +
 * летающие икосаэдры, параллакс по движению мыши. Подпись убрана.
 */
export default function HeroCanvas() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.set(0, 0, 6.2);

    const group = new THREE.Group();
    scene.add(group);

    // Центральный узел — зелёный бренд, глянцевый
    const knot = new THREE.Mesh(
      new THREE.TorusKnotGeometry(1.35, 0.42, 180, 32),
      new THREE.MeshStandardMaterial({ color: 0x3f8a4c, roughness: 0.32, metalness: 0.35 }),
    );
    group.add(knot);

    // Кремовая wireframe-оболочка
    const wire = new THREE.Mesh(
      new THREE.IcosahedronGeometry(2.35, 1),
      new THREE.MeshBasicMaterial({
        color: 0xfbf6e6,
        wireframe: true,
        transparent: true,
        opacity: 0.16,
      }),
    );
    group.add(wire);

    // Летающие маленькие икосаэдры
    const bitGeo = new THREE.IcosahedronGeometry(0.22, 0);
    const bitMat = new THREE.MeshStandardMaterial({ color: 0x9fd0aa, roughness: 0.4, metalness: 0.2 });
    const bits: THREE.Mesh[] = [];
    for (let i = 0; i < 7; i++) {
      const m = new THREE.Mesh(bitGeo, bitMat);
      const a = (i / 7) * Math.PI * 2;
      m.userData.a = a;
      m.userData.r = 2.4 + (i % 3) * 0.35;
      group.add(m);
      bits.push(m);
    }

    scene.add(new THREE.AmbientLight(0xffffff, 0.55));
    const key = new THREE.DirectionalLight(0xffffff, 1.1);
    key.position.set(4, 5, 6);
    scene.add(key);
    const rim = new THREE.DirectionalLight(0x7fb98a, 0.9);
    rim.position.set(-5, -2, -4);
    scene.add(rim);

    const onResize = () => {
      const w = canvas.clientWidth || 1;
      const h = canvas.clientHeight || 1;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    };
    onResize();
    window.addEventListener("resize", onResize);

    const target = { x: 0, y: 0 };
    const cur = { x: 0, y: 0 };
    const onPointer = (e: PointerEvent) => {
      const r = canvas.getBoundingClientRect();
      target.x = ((e.clientX - r.left) / r.width - 0.5) * 0.9;
      target.y = ((e.clientY - r.top) / r.height - 0.5) * 0.9;
    };
    canvas.addEventListener("pointermove", onPointer);

    const clock = new THREE.Clock();
    let raf = 0;
    const loop = () => {
      const t = clock.getElapsedTime();
      knot.rotation.x = t * 0.28;
      knot.rotation.y = t * 0.38;
      wire.rotation.y = -t * 0.12;
      wire.rotation.x = t * 0.06;
      bits.forEach((m, i) => {
        const a = (m.userData.a as number) + t * 0.4;
        const rr = m.userData.r as number;
        m.position.set(Math.cos(a) * rr, Math.sin(a * 1.3 + i) * 1.7, Math.sin(a) * 1.5);
        m.rotation.x = t * (0.6 + i * 0.1);
        m.rotation.y = t * 0.5;
      });
      cur.x += (target.x - cur.x) * 0.05;
      cur.y += (target.y - cur.y) * 0.05;
      group.rotation.y = cur.x;
      group.rotation.x = cur.y;
      renderer.render(scene, camera);
      raf = requestAnimationFrame(loop);
    };
    loop();

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", onResize);
      canvas.removeEventListener("pointermove", onPointer);
      knot.geometry.dispose();
      (knot.material as THREE.Material).dispose();
      wire.geometry.dispose();
      (wire.material as THREE.Material).dispose();
      bitGeo.dispose();
      bitMat.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <div className="relative h-[clamp(340px,44vw,500px)]">
      <div
        className="pointer-events-none absolute inset-[8%_10%] rounded-full blur-[34px]"
        style={{
          background: "radial-gradient(circle, rgba(127,185,138,0.45), transparent 70%)",
          animation: "tm-pulse 5s ease-in-out infinite",
        }}
      />
      <canvas ref={canvasRef} className="relative block h-full w-full" />
    </div>
  );
}
