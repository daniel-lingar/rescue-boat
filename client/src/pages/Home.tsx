import { useState } from "react";
import { useLocation } from "wouter";
import { ChevronDown, ChevronUp, ArrowRight } from "lucide-react";
import {
  ARTICLES,
  ARTICLE_PARTS,
  getArticlesByPart,
} from "@/lib/articles";

export default function Home() {
  const [, setLocation] = useLocation();
  const [expandedPart, setExpandedPart] = useState<string | null>(
    "front-matter"
  );

  const parts = ["front-matter", "counter-narratives", "appendix", "missing-pieces", "resources"] as const;

  return (
    <div className="min-h-screen bg-background">
      {/* Header section with Cover Image */}
      <header className="relative bg-primary overflow-hidden">
        {/* Background Image Overlay */}
        <div className="absolute inset-0 z-0 opacity-40">
          <img 
            src="/rescue-boat/assets/cover.png" 
            alt="" 
            className="w-full h-full object-cover object-center filter blur-sm"
          />
        </div>
        
        <div className="container relative z-10 py-16 md:py-24">
          <div className="flex flex-col md:flex-row gap-12 items-center">
            {/* Main Cover Image */}
            <div className="w-full max-w-[320px] shadow-2xl border-4 border-accent/30 rounded-lg overflow-hidden transform md:-rotate-2 transition-transform hover:rotate-0 duration-500">
              <img 
                src="/rescue-boat/assets/cover.png" 
                alt="The Rescue Boat Book Cover" 
                className="w-full h-auto"
              />
            </div>

            <div className="max-w-2xl text-center md:text-left">
              <h1 className="text-5xl md:text-7xl font-bold text-accent mb-4 font-sans leading-tight border-none pb-0">
                The Rescue Boat
              </h1>
              <h2 className="text-2xl md:text-3xl text-accent/90 mb-6 font-serif italic">
                & Other Counter-Narratives
              </h2>
              <div className="w-24 h-1 bg-accent mb-8 mx-auto md:mx-0"></div>
              <p className="text-xl text-primary-foreground/90 font-serif leading-relaxed mb-6">
                Ten articles on trauma, addiction, and the nervous system
              </p>
              <p className="text-base text-primary-foreground/80 font-serif max-w-xl mb-3">
                This is a survival doctrine. It does not offer comfort. It offers translation.
              </p>
              <p className="text-sm text-primary-foreground/70 font-serif max-w-xl italic">
                The rescue boat is not the enemy — it is proof someone wanted to live. This edition names the storm and offers other tools.
              </p>
            </div>
          </div>
        </div>
        <div className="h-2 bg-accent w-full"></div>
      </header>

      {/* WHAT THIS IS Section */}
      <section className="py-12 md:py-16 bg-card border-b border-border">
        <div className="container max-w-3xl">
          <h2 className="text-3xl font-bold mb-8 font-sans text-accent">What This Is</h2>
          <div className="space-y-6 text-foreground font-serif leading-relaxed">
            <p className="text-xl font-medium italic">
              "This is a survival doctrine. It does not offer comfort. It offers translation."
            </p>
            
            <div className="grid gap-8 md:grid-cols-2">
              <div>
                <h3 className="text-lg font-bold mb-2 font-sans uppercase tracking-wider text-accent">The Problem</h3>
                <p className="text-sm text-muted-foreground">
                  Traditional systems measure compliance. Traumatized nervous systems measure survival. When the two collide, freeze gets labeled defiance, shame gets called conscience, and addiction gets treated as a moral failure.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-bold mb-2 font-sans uppercase tracking-wider text-accent">How It’s Different</h3>
                <p className="text-sm text-muted-foreground">
                  This book replaces <em>what's wrong with you</em> with <em>how did you survive this wiring?</em> It treats trauma responses as outdated threat protocols — not character flaws.
                </p>
              </div>
            </div>

            <div className="p-6 bg-background/50 border border-accent/20 rounded-lg">
              <h3 className="text-lg font-bold mb-3 font-sans text-accent">What Changes</h3>
              <p className="text-sm">
                You stop fighting your biology. You learn to name the protocol. You replace punishment with predictability, shame with data, and isolation with borrowed calm. The goal isn't perfection. It's alignment.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* START HERE Section */}
      <section className="py-12 md:py-16 bg-background">
        <div className="container max-w-4xl">
          <h2 className="text-3xl font-bold mb-4 font-sans text-accent">How to use this edition</h2>
          <p className="mb-6 font-serif text-muted-foreground">
            Pick your path — survivor or systems supporter. You do not have to read in order.
          </p>
          <div className="grid gap-4 md:grid-cols-2 mb-10">
            <div className="p-5 bg-card border border-border rounded-lg">
              <h3 className="font-bold text-accent mb-2">Survivors and peers</h3>
              <p className="text-sm text-muted-foreground">
                Start with Article 1 (<em>The Rescue Boat</em>). Read for recognition. Return to Article 10 when setbacks feel like starting over.
              </p>
            </div>
            <div className="p-5 bg-card border border-border rounded-lg">
              <h3 className="font-bold text-accent mb-2">Supporters and systems</h3>
              <p className="text-sm text-muted-foreground">
                Start with Article 5 (Translation), then Part IV resources — freeze protocol, 26 Laws, harm reduction.
              </p>
            </div>
          </div>
          <h3 className="text-xl font-bold mb-4 font-sans text-accent">Start by state</h3>
          <p className="mb-8 font-serif text-sm text-muted-foreground">Or jump straight to what matches how you feel right now.</p>
          
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            <button 
              onClick={() => setLocation('/article/translation-between-the-system-and-trauma')}
              className="p-6 bg-card border border-border rounded-lg hover:border-accent/50 transition-all text-left group"
            >
              <h3 className="font-bold mb-2 group-hover:text-accent transition-colors">Locked or Shaking?</h3>
              <p className="text-xs text-muted-foreground mb-4">Freeze, withdrawal, punishment — translation for both sides.</p>
              <div className="flex items-center text-xs font-bold text-accent uppercase tracking-widest">
                Go to Translation <ArrowRight className="ml-2 w-3 h-3" />
              </div>
            </button>

            <button 
              onClick={() => setLocation('/article/shame-is-the-glue')}
              className="p-6 bg-card border border-border rounded-lg hover:border-accent/50 transition-all text-left group"
            >
              <h3 className="font-bold mb-2 group-hover:text-accent transition-colors">Drowning in Shame?</h3>
              <p className="text-xs text-muted-foreground mb-4">Name it. Don't argue with it. Use the Core Defaults as a reality check.</p>
              <div className="flex items-center text-xs font-bold text-accent uppercase tracking-widest">
                Go to Reframing <ArrowRight className="ml-2 w-3 h-3" />
              </div>
            </button>

            <button 
              onClick={() => setLocation('/article/i-got-clean-i-didnt-get-free')}
              className="p-6 bg-card border border-border rounded-lg hover:border-accent/50 transition-all text-left group"
            >
              <h3 className="font-bold mb-2 group-hover:text-accent transition-colors">Sober but Stuck?</h3>
              <p className="text-xs text-muted-foreground mb-4">Old loops repeating doesn't mean you're failing. It means you're rewiring.</p>
              <div className="flex items-center text-xs font-bold text-accent uppercase tracking-widest">
                Go to Rewiring <ArrowRight className="ml-2 w-3 h-3" />
              </div>
            </button>

            <button 
              onClick={() => setLocation('/article/translation-between-the-system-and-trauma')}
              className="p-6 bg-card border border-border rounded-lg hover:border-accent/50 transition-all text-left group"
            >
              <h3 className="font-bold mb-2 group-hover:text-accent transition-colors">Work in the System?</h3>
              <p className="text-xs text-muted-foreground mb-4">Courts, probation, treatment. Operational reframes you can use tomorrow.</p>
              <div className="flex items-center text-xs font-bold text-accent uppercase tracking-widest">
                Go to Protocols <ArrowRight className="ml-2 w-3 h-3" />
              </div>
            </button>

            <button 
              onClick={() => setLocation('/article/co-regulation-barriers')}
              className="p-6 bg-card border border-border rounded-lg hover:border-accent/50 transition-all text-left group"
            >
              <h3 className="font-bold mb-2 group-hover:text-accent transition-colors">Rural or Isolated?</h3>
              <p className="text-xs text-muted-foreground mb-4">No steady people nearby. Predictability beats proximity.</p>
              <div className="flex items-center text-xs font-bold text-accent uppercase tracking-widest">
                Go to Scaffolds <ArrowRight className="ml-2 w-3 h-3" />
              </div>
            </button>

            <button 
              onClick={() => setLocation('/article/15-core-defaults')}
              className="p-6 bg-accent/5 border border-accent/20 rounded-lg hover:border-accent/50 transition-all text-left group"
            >
              <h3 className="font-bold mb-2 text-accent">The 15 Defaults</h3>
              <p className="text-xs text-muted-foreground mb-4">A quick-reference for your own wiring.</p>
              <div className="flex items-center text-xs font-bold text-accent uppercase tracking-widest">
                View Rules <ArrowRight className="ml-2 w-3 h-3" />
              </div>
            </button>
          </div>
        </div>
      </section>

      {/* Audience Lanes Section */}
      <section className="py-12 md:py-16 bg-card border-t border-b border-border">
        <div className="container max-w-3xl">
          <h2 className="text-3xl font-bold mb-8 font-sans">Who This Is For</h2>
          
          <div className="space-y-8 text-foreground font-serif leading-relaxed">
            <div className="p-6 bg-background/50 border-l-4 border-accent rounded-r-lg">
              <p className="mb-4">This book stands alone. It also serves three different readers.</p>
              <div className="grid gap-6 md:grid-cols-3 text-sm">
                <div>
                  <p className="font-bold text-accent mb-1 font-sans uppercase tracking-wider">Survivors / Peers</p>
                  <p className="text-muted-foreground">Read for the map, not the manual. Use this to name what you're carrying — not to prove you're fixed.</p>
                </div>
                <div>
                  <p className="font-bold text-accent mb-1 font-sans uppercase tracking-wider">Legal Support</p>
                  <p className="text-muted-foreground">Recognize when "noncompliance" is a nervous system shutdown. Operational reframes for court staff.</p>
                </div>
                <div>
                  <p className="font-bold text-accent mb-1 font-sans uppercase tracking-wider">Clinicians / Providers</p>
                  <p className="text-muted-foreground">Translate physiology into plain language. Explain mechanisms without overpromising outcomes.</p>
                </div>
              </div>
            </div>

            <div className="mt-8 pt-8 border-t border-border grid grid-cols-1 md:grid-cols-2 gap-8 text-sm font-sans">
              <div>
                <p className="font-bold text-accent mb-2 uppercase tracking-widest">Citation & Evidence Note</p>
                <p className="text-muted">
                  This book cites foundational trauma and addiction research. For specific page references and primary studies, consult the Technical Appendix (Part II).
                </p>
              </div>
              <div>
                <p className="font-bold text-accent mb-2 uppercase tracking-widest">About the Author</p>
                <p className="text-muted">
                  Daniel Lingar was born in Davenport, Iowa, and raised in Clarksville, Arkansas. He spent forty-three years living with undiagnosed CPTSD — a condition that was running his life with mechanical precision. He is the co-founder of Capitol Contracts LLC. His memoir, <em>From the Storm to the Fire</em>, is the narrative foundation of the What Really Happened (WRH) curriculum.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Table of contents */}
      <section className="py-12 md:py-16">
        <div className="container max-w-4xl">
          <h2 className="text-3xl font-bold mb-12 font-sans">The Manuscript</h2>
          
          <div className="space-y-12">
            {Object.entries(ARTICLE_PARTS).map(([partId, part]) => (
              <div key={partId} className="border-l-2 border-border pl-8 relative">
                <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-accent border-4 border-background"></div>
                <h3 className="text-xl font-bold mb-2 font-sans uppercase tracking-widest text-accent">
                  {part.title}
                </h3>
                <p className="text-sm text-muted-foreground mb-6 font-serif italic">
                  {part.description}
                </p>

                <div className="grid gap-4">
                  {getArticlesByPart(partId as any).map((article) => (
                    <button
                      key={article.id}
                      onClick={() => setLocation(`/article/${article.slug}`)}
                      className="flex flex-col md:flex-row md:items-center justify-between p-6 bg-card border border-border rounded-lg hover:border-accent/50 transition-all text-left group"
                    >
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-1">
                          <span className="text-xs font-bold text-accent/60 font-sans">
                            {article.id.toString().padStart(2, '0')}
                          </span>
                          <h4 className="font-bold group-hover:text-accent transition-colors">
                            {article.title}
                          </h4>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          {article.subtitle}
                        </p>
                      </div>
                      <div className="mt-4 md:mt-0 md:ml-8 flex items-center gap-4 text-xs text-muted-foreground font-sans whitespace-nowrap">
                        <span className="flex items-center gap-1">
                          {article.readingTime} min read
                        </span>
                        <span className="w-1 h-1 rounded-full bg-border"></span>
                        <span>{article.themes.length} themes</span>
                        <ArrowRight className="w-4 h-4 text-accent opacity-0 group-hover:opacity-100 transition-all transform translate-x-[-10px] group-hover:translate-x-0" />
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-card border-t border-border">
        <div className="container text-center">
          <p className="text-sm text-muted-foreground mb-4">
            Educational peer resource. Not therapy. No disclosure required.
          </p>
          <p className="text-xs text-muted-foreground/60">
            © {new Date().getFullYear()} Capitol Contracts LLC • Clarksville, Arkansas
          </p>
          <div className="mt-8">
            <a 
              href="https://wrh-curriculum.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-accent hover:underline font-sans text-sm font-bold uppercase tracking-widest"
            >
              WRH Master Curriculum
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
