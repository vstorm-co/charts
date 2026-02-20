"""Jinja2 template for generating shadcn/ui Table components.

The table template generates a complete React component with:
- TableCaption for accessibility and context
- TableHeader with sortable headers (optional right alignment for numeric columns)
- TableBody with mapped data rows
- Optional TableFooter with calculated totals

Template variables:
    items_json: JSON string of row data
    headers: List of column header names
    caption: Table caption text
    footer_text: Footer summary keyword (e.g., "Total")
    footer_value: Calculated footer value for the last column

Example:
    ```python
    template = SHADCN_TABLE_TEMPLATE.render(
        items_json=json.dumps([{"name": "Alice", "score": 95}]),
        headers=["name", "score"],
        caption="Student Performance",
        footer_text="Average",
        footer_value=95.0
    )
    ```
"""

from jinja2 import Template

SHADCN_TABLE_TEMPLATE = Template("""
"use client"

import * as React from "react"
import {
  Table,
  TableHeader,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  TableCell,
  TableCaption,
} from "@/components/ui/table"

const items = {{ items_json | safe }}

export default function GeneratedUI() {
  return (
    <Table>
      <TableCaption>{{ caption }}</TableCaption>
      <TableHeader>
        <TableRow>
        {% for header in headers %}
          <TableHead
          {% if loop.last %} className="text-right"
          {% endif %}>
          {{ header | capitalize }}</TableHead>
        {% endfor %}
        </TableRow>
      </TableHeader>
      <TableBody>
        {items.map((item, index) => (
          <TableRow key={index}>
            {% for header in headers %}
            <TableCell
            {% if loop.first %} className="font-medium"
            {% elif loop.last %} className="text-right"
            {% endif %}>
              {item["{{ header }}"]}
            </TableCell>
            {% endfor %}
          </TableRow>
        ))}
      </TableBody>
      {% if footer_text and footer_value %}
      <TableFooter>
        <TableRow>
          <TableCell colSpan={ {{ headers|length - 1 }} }>{{ footer_text }}</TableCell>
          <TableCell className="text-right">{{ footer_value }}</TableCell>
        </TableRow>
      </TableFooter>
      {% endif %}
    </Table>
  )
}
""")
