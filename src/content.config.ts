import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const nullableString = z.string().nullable().optional();
const nullableStringList = z.array(z.string()).nullable().optional();

const catalog = defineCollection({
  loader: glob({ base: "./entries", pattern: "**/*.json" }),
  schema: z.object({
    name: z.string(),
    title: z.string(),
    url: z.url(),
    doi: nullableString,
    bibtex: nullableString,
    description: z.string(),
    date: nullableString,
    data_updated: nullableString,
    version: nullableString,
    license: nullableString,
    language: nullableString,
    package_managers: nullableStringList,
    package_manager: nullableString,
    input_formats: nullableStringList,
    output_formats: nullableStringList,
    topics: z.array(z.string()).min(1),
    type: z.enum(["tool", "database", "paper"]),
    interface: z.union([z.string(), z.array(z.string())]).nullable().optional(),
    workflow_managers: nullableStringList,
    platforms: nullableStringList,
    installation_methods: nullableStringList,
  }),
});

export const collections = { catalog };