"""Standalone Textual TUI draft for Verisaria.

This file is intentionally independent from ``src/verisaria``. It uses only
mock data so the layout and interaction direction can be explored without
touching the engine/runtime code.

Run:
    .venv/bin/python draft/verisaria_tui_mock.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Input, RichLog, Static


Color = Literal["amber", "parchment", "red", "green", "dim"]

AMBER = "#d7a86e"
PARCHMENT = "#cfc6b8"
RED = "#c0504d"
GREEN = "#7faa6e"
DIM = "#77756f"


@dataclass
class MockNpc:
    npc_id: str
    name: str
    role: str
    stance_label: str
    stance_value: int
    status: str


@dataclass
class MockWorldVar:
    label: str
    value: bool | str
    tone: Color


@dataclass
class MockLine:
    kind: Color
    actor: str
    text: str


def _m(markup: str) -> Text:
    return Text.from_markup(markup)


def _esc(text: str) -> str:
    return text.replace("[", "\\[")


def _bar(value: int, width: int = 16) -> str:
    value = max(0, min(100, value))
    filled = round(width * value / 100)
    return "█" * filled + "░" * (width - filled)


def _color(kind: Color) -> str:
    return {
        "amber": AMBER,
        "parchment": PARCHMENT,
        "red": RED,
        "green": GREEN,
        "dim": DIM,
    }[kind]


class VerisariaDraftTui(App[None]):
    """A mock-data TUI prototype for the Frostgate scenario."""

    TITLE = "Verisaria Draft TUI"
    SUB_TITLE = "mock data prototype"
    BINDINGS = [
        Binding("q", "quit", "退出"),
        Binding("m", "toggle_map", "地图"),
        Binding("f", "cycle_focus", "焦点"),
        Binding("w", "flip_world", "世界变量"),
    ]

    CSS = f"""
    Screen {{
        layout: vertical;
        background: #07090c;
        color: {PARCHMENT};
    }}

    #status {{
        height: 3;
        border: round #3a3f47;
        padding: 0 1;
        margin: 0 1 0 1;
        color: {PARCHMENT};
        background: #0b0e12;
    }}

    #main {{
        height: 1fr;
        margin: 0 1;
    }}

    .panel {{
        border: round #3a3f47;
        background: #090c10;
        padding: 0 1;
    }}

    #left {{
        width: 32;
        min-width: 26;
    }}

    #events {{
        width: 1fr;
        min-width: 54;
        padding: 0 1;
    }}

    #right {{
        width: 38;
        min-width: 30;
    }}

    #map {{
        height: 2fr;
    }}

    #focus {{
        height: 1fr;
    }}

    #nearby {{
        height: 2fr;
    }}

    #world {{
        height: 1fr;
    }}

    #agenda {{
        height: 1fr;
    }}

    #input-row {{
        height: 4;
        border: round #3a3f47;
        padding: 0 1;
        margin: 0 1;
        background: #090c10;
    }}

    #command {{
        height: 1;
        border: none;
        background: #05070a;
        color: {PARCHMENT};
    }}
    """

    def __init__(self) -> None:
        super().__init__()
        self.tick = 127
        self.hp = 32
        self.max_hp = 32
        self.stamina = 18
        self.max_stamina = 24
        self.location = "霜门哨所 · 门楼"
        self.pacing = "紧张"
        self._show_map = True
        self._focus_index = 0
        self._turn_index = 0
        self.refugees_admitted = False
        self.npcs = [
            MockNpc("captain_brann", "队长布兰", "霜门指挥官", "信任", 24, "谨慎但公正"),
            MockNpc("sentry_voss", "哨兵沃斯", "哨站哨兵", "紧张", 15, "害怕出错"),
            MockNpc("refugee_kaze", "难民卡泽", "营外难民", "戒备", 36, "隔门观望"),
        ]
        self.world_vars = [
            MockWorldVar("难民入营", False, "red"),
            MockWorldVar("霜门戒备等级", "高", "red"),
            MockWorldVar("补给状况", "吃紧", "amber"),
            MockWorldVar("外部威胁", "上升", "red"),
        ]
        self.focus_lines = [
            "目标：说服队长暂时接纳难民",
            "动机：风雪正在变强，门外有人撑不到天亮",
            "当前策略：以事实与共同风险施压",
        ]

    def compose(self) -> ComposeResult:
        yield Static(id="status")
        with Horizontal(id="main"):
            with Vertical(id="left"):
                yield Static(id="map", classes="panel")
                yield Static(id="focus", classes="panel")
            yield RichLog(id="events", classes="panel", markup=True, wrap=True, highlight=False)
            with Vertical(id="right"):
                yield Static(id="nearby", classes="panel")
                yield Static(id="world", classes="panel")
                yield Static(id="agenda", classes="panel")
        with Vertical(id="input-row"):
            yield Static(id="input-label")
            yield Input(id="command", placeholder="输入自然语言行动…")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#map", Static).border_title = "地图 (m)"
        self.query_one("#focus", Static).border_title = "焦点 (f)"
        self.query_one("#events", RichLog).border_title = "事件流"
        self.query_one("#nearby", Static).border_title = "附近 NPC"
        self.query_one("#world", Static).border_title = "世界状态"
        self.query_one("#agenda", Static).border_title = "玩家议程"
        self.query_one("#input-label", Static).update(_m(f"[{AMBER}]输入[/]"))
        self._refresh_all()
        self._seed_log()
        self.query_one("#command", Input).focus()

    def _seed_log(self) -> None:
        lines = [
            MockLine("dim", "系统", "风雪拍打门洞，火盆里的松枝噼啪作响。"),
            MockLine("parchment", "队长布兰", "这里是霜门。无关人员不得入内。说明来意。"),
            MockLine("red", "压力", "门外难民聚集，哨兵的手一直没离开枪杆。"),
        ]
        for line in lines:
            self._append_line(line)

    def _refresh_all(self) -> None:
        self.query_one("#status", Static).update(_m(self._render_status()))
        self.query_one("#map", Static).update(_m(self._render_map()))
        self.query_one("#focus", Static).update(_m(self._render_focus()))
        self.query_one("#nearby", Static).update(_m(self._render_nearby()))
        self.query_one("#world", Static).update(_m(self._render_world()))
        self.query_one("#agenda", Static).update(_m(self._render_agenda()))

    def _render_status(self) -> str:
        return (
            f"[{RED}]♥[/] 生命 {self.hp}/{self.max_hp}    "
            f"[{AMBER}]⚡[/] 耐力 {self.stamina}/{self.max_stamina}    "
            f"[dim]Tick[/] {self.tick:04d}    "
            f"[dim]位置[/] {self.location}    "
            f"[{AMBER}]节奏 {self.pacing}[/]"
        )

    def _render_map(self) -> str:
        if not self._show_map:
            return "[dim]地图已折叠。[/]"
        return (
            "[dim]         N[/]\n"
            "[dim]    ┌──────────┐[/]\n"
            "[dim]    │  兵营    │[/]\n"
            "[dim]    └────┬─────┘[/]\n"
            f"[{AMBER}]         │[/]\n"
            f"[{AMBER}]    ┌────★────┐[/]\n"
            f"[{AMBER}]    │  门楼   │[/]\n"
            f"[{AMBER}]    └────┬────┘[/]\n"
            "[dim]         │[/]\n"
            "[dim]    ┌────○────┐[/]\n"
            "[dim]    │ 难民营  │[/]\n"
            "[dim]    └─────────┘[/]\n"
            "\n[dim]★ 当前  ○ 可前往[/]"
        )

    def _render_focus(self) -> str:
        focus = self.focus_lines[self._focus_index]
        return (
            f"[{AMBER}]{_esc(focus)}[/]\n\n"
            "[dim]可见事实[/]\n"
            "· 守军补给不足\n"
            "· 难民仍在门外\n"
            "· 队长拥有开门权限"
        )

    def _render_nearby(self) -> str:
        rows = []
        for npc in self.npcs[:2]:
            color = GREEN if npc.stance_label in ("信任", "好感") else RED if npc.stance_label in ("紧张", "戒备") else AMBER
            rows.append(
                f"[bold {PARCHMENT}]{npc.name}[/] [dim]({npc.npc_id})[/]\n"
                f"  [dim]{npc.role}[/]\n"
                f"  {npc.stance_label} [{color}]{_bar(npc.stance_value)}[/] {npc.stance_value}/100\n"
                f"  [dim]{npc.status}[/]"
            )
        return "\n\n".join(rows)

    def _render_world(self) -> str:
        rows = []
        for var in self.world_vars:
            value = self.refugees_admitted if var.label == "难民入营" else var.value
            tone = "green" if value is True else var.tone
            rendered = "true" if value is True else "false" if value is False else str(value)
            rows.append(f"{var.label:<8} [{_color(tone)}]{_esc(rendered)}[/]")
        return "\n".join(rows)

    def _render_agenda(self) -> str:
        return (
            f"[{AMBER}]接纳难民[/] [dim]已反复表达[/]\n"
            "[dim]未解问题[/]\n"
            "· 队长会为谁承担风险？\n"
            "· 教会宣传有多少是真的？"
        )

    def _append_line(self, line: MockLine) -> None:
        color = _color(line.kind)
        prefix = f"[dim]{self.tick:04d}[/] "
        if line.actor == "你":
            markup = f"{prefix}[{AMBER}]你：{_esc(line.text)}[/]"
        elif line.actor == "压力":
            markup = f"{prefix}[{RED}]压力：{_esc(line.text)}[/]"
        elif line.actor == "世界变化":
            markup = f"{prefix}[{GREEN}]世界变化：{_esc(line.text)}[/]"
        elif line.actor == "系统":
            markup = f"{prefix}[dim]{_esc(line.text)}[/]"
        else:
            markup = f"{prefix}[{color}]{_esc(line.actor)}：{_esc(line.text)}[/]"
        self.query_one("#events", RichLog).write(markup)

    def on_input_submitted(self, message: Input.Submitted) -> None:
        text = message.value.strip()
        message.input.value = ""
        if not text:
            text = "等待片刻，观察门楼里的动静。"

        self.tick += 1
        self.stamina = max(0, self.stamina - 1)
        self._turn_index += 1
        message.input.disabled = True
        message.input.placeholder = "（正在领会你的意思…）"
        self._append_line(MockLine("amber", "你", text))
        self._refresh_all()

        script = self._script_for_turn(text)
        for index, line in enumerate(script, start=1):
            self.set_timer(0.18 * index, lambda line=line: self._append_line(line))
        self.set_timer(0.18 * (len(script) + 1), self._finish_mock_turn)

    def _script_for_turn(self, text: str) -> list[MockLine]:
        if self._turn_index % 3 == 1:
            self.npcs[0].stance_value = min(100, self.npcs[0].stance_value + 8)
            self.npcs[1].stance_value = min(100, self.npcs[1].stance_value + 6)
            return [
                MockLine("parchment", "队长布兰", "你的话听起来慷慨，但我要守的是整座哨站。"),
                MockLine("red", "压力", "哨兵沃斯看向门外，难民队伍里有人倒在雪地上。"),
                MockLine("green", "关系", "队长布兰 信任 +0.08；哨兵沃斯 紧张 +0.06"),
            ]
        if self._turn_index % 3 == 2:
            self.refugees_admitted = True
            self.npcs[0].status = "默许有限接纳"
            return [
                MockLine("parchment", "队长布兰", "好吧。先让孩子和伤者进来，其他人等我的命令。"),
                MockLine("green", "世界变化", "难民入营 false → true"),
                MockLine("red", "压力", "补给压力上升，兵营里传来压低的争吵声。"),
            ]
        return [
            MockLine("parchment", "哨兵沃斯", "如果教会追究下来，没人会替我们说话。"),
            MockLine("dim", "系统", "风声盖过了远处难民营的一阵咳嗽。"),
            MockLine("amber", "目标", "你逐渐确信：接纳难民是眼前最重要的事。"),
        ]

    def _finish_mock_turn(self) -> None:
        command = self.query_one("#command", Input)
        command.disabled = False
        command.placeholder = "输入自然语言行动…"
        command.focus()
        self._refresh_all()

    def action_toggle_map(self) -> None:
        self._show_map = not self._show_map
        self._refresh_all()

    def action_cycle_focus(self) -> None:
        self._focus_index = (self._focus_index + 1) % len(self.focus_lines)
        self._refresh_all()

    def action_flip_world(self) -> None:
        self.refugees_admitted = not self.refugees_admitted
        self._append_line(
            MockLine(
                "green",
                "世界变化",
                f"难民入营 → {'true' if self.refugees_admitted else 'false'}",
            )
        )
        self._refresh_all()


if __name__ == "__main__":
    VerisariaDraftTui().run()
