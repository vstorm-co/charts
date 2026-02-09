from jinja2 import Template

SHADCN_CAROUSEL_TEMPLATE = Template("""
"use client"
import * as React from "react"
import { Card, CardContent } from "@/components/ui/card"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"

const items = {{ items_json }}

export default function GeneratedCarousel() {
  return (
    <Carousel
      opts={ {
      align: "{{ align | default('start') }}",
      loop: {{ loop | default('true') }}
      } }
      orientation="{{ orientation | default('horizontal') }}"
      {# Vertical carousels in Shadcn require a container height #}
      className="w-full {{ container_class | default('max-w-xs') }} {% if orientation == 'vertical' %}h-[400px]{% endif %}"
    >
      <CarouselContent {% if orientation == 'vertical' %}className="-mt-1 h-[400px]"{% endif %}>
        {items.map((item, index) => (
          <CarouselItem key={index} className="{{ item_class | default('') }}">
            <div className="p-1">
              <Card>
                <CardContent className="flex aspect-square items-center justify-center p-6">
                  <span className="text-4xl font-semibold">
                    {item.content || (index + 1)}
                  </span>
                </CardContent>
              </Card>
            </div>
          </CarouselItem>
        ))}
      </CarouselContent>
      <CarouselPrevious />
      <CarouselNext />
    </Carousel>
  )
}
""")
