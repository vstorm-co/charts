from jinja2 import Template

SHADCN_CAROUSEL_TEMPLATE = Template("""
"use client"

import * as React from "react"

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter } from "@/components/ui/card"

import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts'

const items = {{ items_json }}

export default function GeneratedCarousel() {
  return (
    <Carousel
      opts={ {
        align: "{{ align | default('start') }}",
        loop: {{ 'true' if loop else 'false' }}
      } }
      orientation="{{ orientation | default('horizontal') }}"
      className="w-full {{ container_class | default('max-w-md mx-auto') }}
      {% if orientation == 'vertical' %}h-[400px]{% endif %}"
    >
      <CarouselContent {% if orientation == 'vertical' %}className="-mt-1 h-[400px]"{% endif %}>
        {items.map((item, index) => {
          const content = item.content;

          return (
            <CarouselItem key={index} className="{{ item_class | default('') }}">
              <div className="p-2 h-full">
                {/* --- COMPONENT DISPATCHER --- */}

                {/* 1. RENDER CARD */}
                {content?.component_type === 'card' && (
                  <Card className="h-full flex flex-col">
                    <CardHeader>
                      <CardTitle className="text-xl">{content.title}</CardTitle>
                      {content.description &&
                      <CardDescription>{content.description}
                      </CardDescription>}
                    </CardHeader>
                    <CardContent className="flex-grow text-sm">
                      {content.content}
                    </CardContent>
                    {content.footer && (
                      <CardFooter className="text-xs text-muted-foreground border-t pt-2">
                        {content.footer}
                      </CardFooter>
                    )}
                  </Card>
                )}

                {/* FALLBACK (Simple String or Index) */}
                {!content?.component_type && (
                   <Card className="flex aspect-square items-center justify-center p-6">
                     <span className="text-4xl font-semibold">
                       {typeof content === 'string' ? content : (index + 1)}
                     </span>
                   </Card>
                )}
              </div>
            </CarouselItem>
          );
        })}
      </CarouselContent>
      <CarouselPrevious />
      <CarouselNext />
    </Carousel>
  )
}
""")
