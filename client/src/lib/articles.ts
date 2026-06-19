export interface Article {
  id: number;
  slug: string;
  title: string;
  subtitle: string;
  part: "front-matter" | "counter-narratives" | "appendix" | "missing-pieces" | "resources";
  contentFile: string;
  readingTime: number;
  themes: string[];
  relatedArticles: number[];
}

export const ARTICLES: Article[] = [
  {
    id: 0,
    slug: "how-to-use",
    title: "How to Use This Book",
    subtitle: "Two paths: survivor/peer or systems/supporter",
    part: "front-matter",
    contentFile: "how_to_use.md",
    readingTime: 3,
    themes: ["Guide", "Audience", "Navigation"],
    relatedArticles: [1, 5],
  },
  {
    id: 1,
    slug: "the-rescue-boat",
    title: "The Rescue Boat",
    subtitle: "Addiction is survival, not weakness",
    part: "counter-narratives",
    contentFile: "article_01.md",
    readingTime: 12,
    themes: ["Addiction", "Survival", "Nervous System", "Self-Medication"],
    relatedArticles: [4, 6, 10],
  },
  {
    id: 2,
    slug: "shame-is-the-glue",
    title: "Shame Is the Glue",
    subtitle: "Shame motivates hiding, not change",
    part: "counter-narratives",
    contentFile: "article_02.md",
    readingTime: 10,
    themes: ["Shame", "Behavior Change", "Nervous System", "Healing"],
    relatedArticles: [7, 1, 10],
  },
  {
    id: 3,
    slug: "staying-stoic-is-a-cage",
    title: "Staying Stoic Is a Cage",
    subtitle: "Stoicism is suffocation, not strength",
    part: "counter-narratives",
    contentFile: "article_03.md",
    readingTime: 13,
    themes: ["Emotional Suppression", "Freeze", "Vulnerability", "Co-Regulation"],
    relatedArticles: [8, 5, 10],
  },
  {
    id: 4,
    slug: "i-got-clean-i-didnt-get-free",
    title: "I Got Clean. I Didn't Get Free.",
    subtitle: "Sobriety is the starting gate, not the finish line",
    part: "counter-narratives",
    contentFile: "article_04.md",
    readingTime: 12,
    themes: ["Sobriety", "Freedom", "Healing", "Nervous System Regulation"],
    relatedArticles: [1, 5, 10],
  },
  {
    id: 5,
    slug: "translation-between-the-system-and-trauma",
    title: "Translation Between the System and Trauma",
    subtitle: "Freeze is not defiance. Consequences don't teach — they trigger.",
    part: "counter-narratives",
    contentFile: "article_05.md",
    readingTime: 18,
    themes: [
      "Freeze Response",
      "Legal System",
      "Withdrawal",
      "Punishment",
      "Translation",
    ],
    relatedArticles: [2, 3, 4],
  },
  {
    id: 6,
    slug: "normal-is-the-most-addictive-state",
    title: "Normal Is the Most Addictive State",
    subtitle: "Addicts chase normal, not highs",
    part: "counter-narratives",
    contentFile: "article_06.md",
    readingTime: 11,
    themes: ["Addiction", "Baseline", "Nervous System", "Self-Medication"],
    relatedArticles: [1, 4, 10],
  },
  {
    id: 7,
    slug: "the-mirror-lies",
    title: "The Mirror Lies",
    subtitle: "Shame distorts everything. Trust the data, not the feeling.",
    part: "counter-narratives",
    contentFile: "article_07.md",
    readingTime: 10,
    themes: ["Shame", "Self-Perception", "Trauma", "Healing"],
    relatedArticles: [2, 1, 10],
  },
  {
    id: 8,
    slug: "i-needed-a-co-regulator",
    title: "I Needed a Co-Regulator, Not a Savior",
    subtitle: "Find a steady presence, not a rescuer",
    part: "counter-narratives",
    contentFile: "article_08.md",
    readingTime: 11,
    themes: ["Co-Regulation", "Relationships", "Nervous System", "Healing"],
    relatedArticles: [3, 10, 4],
  },
  {
    id: 9,
    slug: "you-cant-outrun-your-nervous-system",
    title: "You Can't Outrun Your Nervous System",
    subtitle: "The fire follows you. You have to face it.",
    part: "counter-narratives",
    contentFile: "article_09.md",
    readingTime: 12,
    themes: ["Nervous System", "Trauma Response", "Integration", "Healing"],
    relatedArticles: [10, 1, 3],
  },
  {
    id: 10,
    slug: "healing-is-a-spiral",
    title: "Healing Is a Spiral",
    subtitle: "Setbacks are not resets.",
    part: "counter-narratives",
    contentFile: "article_10.md",
    readingTime: 11,
    themes: ["Healing", "Setbacks", "Progress", "Integration"],
    relatedArticles: [9, 4, 8],
  },
  {
    id: 11,
    slug: "deep-science-and-reframes",
    title: "Deep Science and Reframes",
    subtitle: "Citations, neurobiology, and the research behind the counter-narratives",
    part: "appendix",
    contentFile: "appendix.md",
    readingTime: 15,
    themes: ["Neuroscience", "Research", "Citations", "Evidence"],
    relatedArticles: [],
  },
  {
    id: 12,
    slug: "what-the-system-leaves-out",
    title: "What the System Leaves Out",
    subtitle: "The tools and reframes that traditional systems overlook",
    part: "missing-pieces",
    contentFile: "missing_pieces_overview.md",
    readingTime: 8,
    themes: ["Systems", "Tools", "Reframes", "Recovery"],
    relatedArticles: [5],
  },
  {
    id: 13,
    slug: "freeze-response-protocol",
    title: "Freeze Response Protocol for Courtrooms",
    subtitle: "Operational reframes for legal support staff",
    part: "resources",
    contentFile: "freeze_protocol.md",
    readingTime: 5,
    themes: ["Legal System", "Freeze Response", "Protocol"],
    relatedArticles: [5],
  },
  {
    id: 14,
    slug: "the-26-laws-of-survival",
    title: "The 26 Laws of Survival",
    subtitle: "Heuristic tools for pattern recognition",
    part: "resources",
    contentFile: "26_laws.md",
    readingTime: 10,
    themes: ["Survival", "Laws", "Pattern Recognition"],
    relatedArticles: [],
  },
  {
    id: 15,
    slug: "harm-reduction-note",
    title: "Harm Reduction Note",
    subtitle: "Regulation, not perfection",
    part: "resources",
    contentFile: "harm_reduction.md",
    readingTime: 3,
    themes: ["Harm Reduction", "Regulation", "Addiction"],
    relatedArticles: [1, 6],
  },
  {
    id: 16,
    slug: "co-regulation-barriers",
    title: "Co-Regulation Barriers & Low-Bar Alternatives",
    subtitle: "Building scaffolds for connection",
    part: "resources",
    contentFile: "co_regulation_barriers.md",
    readingTime: 4,
    themes: ["Co-Regulation", "Barriers", "Connection"],
    relatedArticles: [8, 3],
  },
  {
    id: 17,
    slug: "15-core-defaults",
    title: "The 15 Core Defaults",
    subtitle: "Rules of the system",
    part: "resources",
    contentFile: "15_defaults.md",
    readingTime: 5,
    themes: ["Principles", "System Rules", "Regulation"],
    relatedArticles: [],
  },
];

export const ARTICLE_PARTS = {
  "front-matter": {
    title: "START HERE",
    description: "How to read this edition for your role",
  },
  "counter-narratives": {
    title: "PART I: THE COUNTER-NARRATIVES",
    description: "Ten articles challenging the narratives that shame and blame survivors",
  },
  appendix: {
    title: "PART II: TECHNICAL APPENDIX",
    description: "Citations, neurobiology, and the research behind the counter-narratives",
  },
  "missing-pieces": {
    title: "PART III: THE SEVEN MISSING PIECES",
    description: "The tools and reframes that traditional systems overlook",
  },
  resources: {
    title: "ADDITIONAL RESOURCES",
    description: "Protocols, laws, and practical tools for survival and support",
  },
};

export function getArticleById(id: number): Article | undefined {
  return ARTICLES.find((article) => article.id === id);
}

export function getArticleBySlug(slug: string): Article | undefined {
  return ARTICLES.find((article) => article.slug === slug);
}

export function getArticlesByPart(
  part: "front-matter" | "counter-narratives" | "appendix" | "missing-pieces" | "resources"
): Article[] {
  return ARTICLES.filter((article) => article.part === part);
}

export function getNextArticle(currentId: number): Article | undefined {
  const currentIndex = ARTICLES.findIndex((a) => a.id === currentId);
  if (currentIndex === -1 || currentIndex === ARTICLES.length - 1) return undefined;
  return ARTICLES[currentIndex + 1];
}

export function getPreviousArticle(currentId: number): Article | undefined {
  const currentIndex = ARTICLES.findIndex((a) => a.id === currentId);
  if (currentIndex <= 0) return undefined;
  return ARTICLES[currentIndex - 1];
}