#!/usr/bin/env bash
# motion-design — emit microinteraction starter snippets
set -euo pipefail

usage() { cat <<EOF
motion-design — snippet generator
  snippet.sh list
  snippet.sh <pattern> [--lib framer|css|gsap]

Patterns: fade-in slide-up scale-in modal drawer toast accordion
          skeleton shake confetti magnetic-button stagger-list
EOF
}

PATTERN="${1:-}"
LIB="framer"
shift || true
while [ $# -gt 0 ]; do case "$1" in --lib) LIB="$2"; shift 2;; *) shift;; esac; done

[ -z "$PATTERN" ] && { usage; exit 1; }

case "$PATTERN" in
  list)
    echo "fade-in slide-up scale-in modal drawer toast accordion skeleton shake confetti magnetic-button stagger-list" | tr ' ' '\n'
    exit 0;;
esac

emit() { cat; }

case "$LIB:$PATTERN" in
  framer:fade-in) emit <<'X'
import { motion } from "framer-motion";
<motion.div initial={{opacity:0}} animate={{opacity:1}}
  transition={{duration:0.3, ease:[0,0,0.2,1]}}>...</motion.div>
X
  ;;
  framer:slide-up) emit <<'X'
<motion.div initial={{opacity:0, y:16}} animate={{opacity:1, y:0}}
  transition={{duration:0.3, ease:[0,0,0.2,1]}}>...</motion.div>
X
  ;;
  framer:scale-in) emit <<'X'
<motion.div initial={{opacity:0, scale:0.96}} animate={{opacity:1, scale:1}}
  transition={{type:"spring", stiffness:300, damping:30}}>...</motion.div>
X
  ;;
  framer:modal) emit <<'X'
import { AnimatePresence, motion } from "framer-motion";
<AnimatePresence>
  {open && (
    <motion.div className="fixed inset-0 bg-black/50"
      initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}} />
  )}
  {open && (
    <motion.div className="fixed inset-0 grid place-items-center"
      initial={{opacity:0, y:8, scale:0.98}}
      animate={{opacity:1, y:0, scale:1}}
      exit={{opacity:0, y:8, scale:0.98}}
      transition={{duration:0.25}}>
      <div className="bg-white rounded-xl p-6">...</div>
    </motion.div>
  )}
</AnimatePresence>
X
  ;;
  framer:drawer) emit <<'X'
<motion.div drag="x" dragConstraints={{left:0, right:0}}
  initial={{x:"-100%"}} animate={{x:0}} exit={{x:"-100%"}}
  transition={{type:"spring", stiffness:400, damping:40}}
  className="fixed left-0 top-0 h-full w-80 bg-white shadow-xl">...</motion.div>
X
  ;;
  framer:toast) emit <<'X'
<motion.div initial={{opacity:0, y:24, scale:0.96}}
  animate={{opacity:1, y:0, scale:1}}
  exit={{opacity:0, y:24, scale:0.96}}
  transition={{type:"spring", stiffness:400, damping:40}}>
  Toast text
</motion.div>
X
  ;;
  framer:accordion) emit <<'X'
import { motion, AnimatePresence } from "framer-motion";
<AnimatePresence initial={false}>
  {open && (
    <motion.section
      initial={{height:0, opacity:0}}
      animate={{height:"auto", opacity:1}}
      exit={{height:0, opacity:0}}
      transition={{duration:0.25}}
      style={{overflow:"hidden"}}>
      ...content
    </motion.section>
  )}
</AnimatePresence>
X
  ;;
  framer:stagger-list) emit <<'X'
const container = { animate: { transition: { staggerChildren: 0.05 } } };
const item = { initial:{opacity:0,y:8}, animate:{opacity:1,y:0} };
<motion.ul variants={container} initial="initial" animate="animate">
  {items.map(i=> <motion.li key={i.id} variants={item}>{i.label}</motion.li>)}
</motion.ul>
X
  ;;
  framer:magnetic-button) emit <<'X'
import { motion, useMotionValue, useSpring } from "framer-motion";
function Magnetic({children}) {
  const x = useMotionValue(0), y = useMotionValue(0);
  const sx = useSpring(x, {stiffness:200, damping:15});
  const sy = useSpring(y, {stiffness:200, damping:15});
  return (
    <motion.button style={{x:sx, y:sy}}
      onPointerMove={e=>{const r=e.currentTarget.getBoundingClientRect();
        x.set((e.clientX-r.left-r.width/2)*0.3);
        y.set((e.clientY-r.top-r.height/2)*0.3);}}
      onPointerLeave={()=>{x.set(0); y.set(0);}}>
      {children}
    </motion.button>
  );
}
X
  ;;
  framer:shake) emit <<'X'
<motion.div animate={shake?{x:[-8,8,-6,6,-3,3,0]}:{}} transition={{duration:0.4}}/>
X
  ;;
  css:fade-in) emit <<'X'
.fade-in { opacity:0; animation: fade-in .3s cubic-bezier(0,0,.2,1) forwards; }
@keyframes fade-in { to { opacity:1; } }
@media (prefers-reduced-motion: reduce) { .fade-in { animation: none; opacity:1; } }
X
  ;;
  css:slide-up) emit <<'X'
.slide-up { transform: translateY(16px); opacity:0;
  animation: slide-up .3s cubic-bezier(0,0,.2,1) forwards; }
@keyframes slide-up { to { transform: none; opacity:1; } }
X
  ;;
  css:skeleton) emit <<'X'
.skeleton {
  background: linear-gradient(90deg,#eee 0%,#f5f5f5 50%,#eee 100%);
  background-size:200% 100%;
  animation: shimmer 1.4s ease-in-out infinite;
}
@keyframes shimmer { from{background-position:200% 0;} to{background-position:-200% 0;} }
@media (prefers-reduced-motion: reduce){ .skeleton{ animation:none; background:#eee; } }
X
  ;;
  css:shake) emit <<'X'
.shake { animation: shake .4s; }
@keyframes shake { 0%,100%{transform:none;}
  20%{transform:translateX(-8px);} 40%{transform:translateX(8px);}
  60%{transform:translateX(-4px);} 80%{transform:translateX(4px);} }
X
  ;;
  gsap:confetti) emit <<'X'
import gsap from "gsap";
function confetti(el) {
  const N = 40;
  for (let i=0;i<N;i++) {
    const p = document.createElement("div");
    p.className = "absolute w-2 h-2 rounded-sm";
    p.style.background = `hsl(${Math.random()*360},80%,60%)`;
    el.appendChild(p);
    gsap.fromTo(p,
      {x:0,y:0,opacity:1},
      {x:(Math.random()-0.5)*400, y:(Math.random()-1)*400,
       rotate:Math.random()*720, opacity:0, duration:1+Math.random(),
       ease:"power3.out", onComplete:()=>p.remove()});
  }
}
X
  ;;
  *)
    echo "ERR: no snippet for lib=$LIB pattern=$PATTERN"
    echo "Run: snippet.sh list"
    exit 1;;
esac
