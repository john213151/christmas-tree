import math
import random
import pygame


# 초기화 및 화면 설정
pygame.init()
WIDTH, HEIGHT = 800, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Neon Particle Christmas Tree - Happy New Year")
clock = pygame.time.Clock()

# 폰트 설정
try:
    font = pygame.font.SysFont("arial", 46, bold=True)
except Exception:
    font = pygame.font.Font(None, 54)

tree_particles = []      # 회전하는 파티클 (나뭇잎 + 나무 몸통)
gift_particles = []      # 고정된 파티클 (선물 상자)
snowman_particles = []   # 고정된 파티클 (여러 크기의 눈사람들)
sleigh_particles = []    # 궤도 비행 파티클 (산타 썰매 + 루돌프/사슴)
falling_gifts = []       # 산타가 떨어뜨리는 3D 선물 꾸러미 리스트

# 1. 3D 트리 나뭇잎 & 오너먼트 파티클 생성
num_particles = 1200
for i in range(num_particles):
    progress = i / num_particles  # 0(꼭대기) ~ 1(바닥)
    y = -280 + progress * 540
    radius = progress * 220
    angle = progress * 35 * math.pi

    r_offset = radius + random.uniform(-12, 12)
    x = r_offset * math.cos(angle)
    z = r_offset * math.sin(angle)

    if random.random() < 0.12:
        color = random.choice(
            [(255, 60, 80), (255, 215, 0), (80, 200, 255), (255, 100, 255)]
        )
        size = random.uniform(3.0, 4.5)
        is_glow = True
    else:
        color = (random.randint(20, 80), random.randint(200, 255), random.randint(100, 170))
        size = random.uniform(1.5, 2.8)
        is_glow = True

    tree_particles.append([x, y, z, color, size, random.uniform(0, math.pi * 2), is_glow])

# 2. 가운데 나무 몸통(Trunk) 원기둥 파티클 생성 (트리와 함께 회전)
for _ in range(350):
    ty = random.uniform(255, 345)
    t_angle = random.uniform(0, 2 * math.pi)
    t_radius = random.uniform(24, 34)
    tx = t_radius * math.cos(t_angle)
    tz = t_radius * math.sin(t_angle)
    t_color = (random.randint(135, 175), random.randint(75, 105), random.randint(35, 55))
    tree_particles.append([tx, ty, tz, t_color, random.uniform(2.0, 3.0), 0, False])

# 3. 주변 선물 상자(Gift Boxes) 생성 함수 (회전하지 않고 고정)
def create_gift_box(cx, cz, width, height, depth, box_color, ribbon_color, yaw_deg=0):
    yaw = math.radians(yaw_deg)
    cos_y, sin_y = math.cos(yaw), math.sin(yaw)
    base_y = 345

    for _ in range(320):
        face = random.randint(0, 5)
        u = random.uniform(-0.5, 0.5)
        v = random.uniform(-0.5, 0.5)

        if face == 0:    lx, ly, lz = u * width, -height, v * depth
        elif face == 1:  lx, ly, lz = u * width, 0, v * depth
        elif face == 2:  lx, ly, lz = u * width, (v - 0.5) * height, depth / 2
        elif face == 3:  lx, ly, lz = u * width, (v - 0.5) * height, -depth / 2
        elif face == 4:  lx, ly, lz = width / 2, (v - 0.5) * height, u * depth
        else:            lx, ly, lz = -width / 2, (v - 0.5) * height, u * depth

        is_ribbon = False
        if face in (0, 1) and (abs(lx) < width * 0.14 or abs(lz) < depth * 0.14):
            is_ribbon = True
        elif face in (2, 3) and abs(lx) < width * 0.14:
            is_ribbon = True
        elif face in (4, 5) and abs(lz) < depth * 0.14:
            is_ribbon = True

        rx = lx * cos_y - lz * sin_y + cx
        rz = lx * sin_y + lz * cos_y + cz
        ry = base_y + ly

        color = ribbon_color if is_ribbon else box_color
        gift_particles.append([rx, ry, rz, color, 2.3 if is_ribbon else 1.9, random.uniform(0, 6.28), is_ribbon])

# 선물 상자 4개 배치
create_gift_box(-135, 95,  68, 55, 68, (230, 45, 75),  (255, 220, 60), 25)    # 왼쪽 앞 빨간 상자
create_gift_box(135,  85,  78, 46, 62, (45, 130, 245), (255, 255, 255), -20)  # 오른쪽 앞 파란 상자
create_gift_box(-85, -85,  58, 68, 58, (180, 65, 240), (255, 215, 0), 35)     # 왼쪽 뒤 보라 상자
create_gift_box(95,  -75,  62, 52, 62, (245, 195, 40), (235, 40, 60), -30)    # 오른쪽 뒤 금색 상자

# 4. 크고 작은 3D 눈사람(Snowman) 생성 함수 (scale_factor로 크기 조절 가능)
def create_snowman(cx, cz, scale_factor=1.0, scarf_color=(255, 50, 75), yaw_deg=-25):
    yaw = math.radians(yaw_deg)
    cos_y, sin_y = math.cos(yaw), math.sin(yaw)
    base_y = 345

    def add_pt(lx, ly, lz, color, size, glow=False):
        sx_l = lx * scale_factor
        sy_l = ly * scale_factor
        sz_l = lz * scale_factor
        rx = sx_l * cos_y - sz_l * sin_y + cx
        rz = sx_l * sin_y + sz_l * cos_y + cz
        ry = base_y + sy_l
        p_size = max(1.4, size * (0.7 + 0.3 * scale_factor))
        snowman_particles.append([rx, ry, rz, color, p_size, random.uniform(0, 6.28), glow])

    # 눈덩이 3단 (하단, 중단, 머리) - 크기에 따라 파티클 수도 조절
    pt_scale = max(0.55, scale_factor)
    tiers = [
        (-36, 38, int(250 * pt_scale)),   # 하단 몸통
        (-86, 28, int(190 * pt_scale)),   # 상단 몸통
        (-125, 20, int(140 * pt_scale)),  # 머리
    ]
    for cy, radius, count in tiers:
        for _ in range(count):
            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)
            r = radius * random.uniform(0.92, 1.02)
            lx = r * math.sin(phi) * math.cos(theta)
            ly = cy + r * math.cos(phi)
            lz = r * math.sin(phi) * math.sin(theta)
            c = (random.randint(225, 250), random.randint(235, 255), 255)
            add_pt(lx, ly, lz, c, random.uniform(2.0, 2.8), False)

    # 네온 목도리
    for _ in range(int(85 * pt_scale)):
        theta = random.uniform(0, 2 * math.pi)
        r = random.uniform(21, 25)
        lx = r * math.cos(theta)
        ly = -106 + random.uniform(-3, 3)
        lz = r * math.sin(theta)
        add_pt(lx, ly, lz, scarf_color, 2.5, True)
    # 목도리 자락
    for i in range(int(22 * pt_scale)):
        add_pt(14 + random.uniform(-2, 2), -104 + i * 1.1, 18 + random.uniform(-2, 2), scarf_color, 2.4, True)

    # 검은 중절모 (챙 + 몸통)
    for _ in range(int(65 * pt_scale)):
        theta = random.uniform(0, 2 * math.pi)
        r = random.uniform(14, 27)
        add_pt(r * math.cos(theta), -143, r * math.sin(theta), (45, 50, 65), 2.2, False)
    for _ in range(int(75 * pt_scale)):
        theta = random.uniform(0, 2 * math.pi)
        h = random.uniform(0, 22)
        add_pt(15 * math.cos(theta), -143 - h, 15 * math.sin(theta), (45, 50, 65), 2.2, False)

    # 당근 코 (앞쪽 +Z 방향)
    for i in range(16):
        t = i / 16
        add_pt(0, -125, 19 + t * 16, (255, 135, 20), 2.8 * (1 - t * 0.5), True)

    # 눈 & 단추
    add_pt(-7, -131, 18.5, (20, 25, 35), 3.0, False)
    add_pt(7, -131, 18.5, (20, 25, 35), 3.0, False)
    for by in (-94, -82, -70):
        add_pt(0, by, 27.5, (30, 35, 45), 2.8, False)

    # 나뭇가지 양팔
    for i in range(20):
        t = i / 20
        add_pt(-25 - t * 26, -90 - t * 14, 0, (140, 85, 45), 2.1, False)
        add_pt(25 + t * 26, -90 - t * 14, 0, (140, 85, 45), 2.1, False)

# 트리에서 떨어진 위치에 크고 작은 눈사람 4개 배치
create_snowman(285,  45,  scale_factor=1.15, scarf_color=(255, 50, 75),   yaw_deg=-35)  # 오른쪽 큰 아빠 눈사람
create_snowman(235, 125,  scale_factor=0.65, scarf_color=(60, 210, 255),  yaw_deg=-20)  # 오른쪽 앞 작은 아기 눈사람
create_snowman(-280, 55,  scale_factor=0.95, scarf_color=(80, 240, 140),  yaw_deg=35)   # 왼쪽 중간 크기 눈사람
create_snowman(-235, 135, scale_factor=0.58, scarf_color=(255, 200, 50),  yaw_deg=25)   # 왼쪽 앞 꼬마 눈사람

# 5. 산타 썰매 & 루돌프/사슴 파티클 모델 생성 (로컬 X축이 진행 방향)
def build_santa_sleigh_and_reindeer():
    # (A) 산타 썰매 본체 (로컬 x: -115 ~ -65)
    for _ in range(180):
        lx = random.uniform(-115, -68)
        lz = random.uniform(-16, 16)
        if random.random() < 0.45:
            ly = 8
        else:
            lz = random.choice([-16, 16])
            ly = random.uniform(-10, 8)
            if lx < -105:
                ly -= 6
        sleigh_particles.append([lx, ly, lz, (240, 40, 65), 2.2, random.uniform(0, 6.28), True, 0])

    # 금빛 썰매 날
    for side in (-14, 14):
        for i in range(35):
            t = i / 34
            lx = -118 + t * 58
            ly = 15 - (8 if t > 0.82 else 0)
            sleigh_particles.append([lx, ly, side, (255, 215, 60), 2.2, 0, True, 0])

    # 선물 보따리
    for _ in range(65):
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        r = random.uniform(0, 12)
        sleigh_particles.append([
            -102 + r * math.sin(phi) * math.cos(theta),
            -6 + r * math.cos(phi),
            r * math.sin(phi) * math.sin(theta),
            (60, 210, 120), 2.2, 0, True, 0
        ])

    # 산타클로스
    for _ in range(75):
        theta = random.uniform(0, 2 * math.pi)
        ly = random.uniform(-18, 2)
        r = 10 * (1 - (-ly) / 28)
        sleigh_particles.append([-82 + r * math.cos(theta), ly, r * math.sin(theta), (255, 45, 65), 2.4, 0, True, 0])
    for _ in range(35):
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        r = 6.5
        sleigh_particles.append([
            -82 + r * math.sin(phi) * math.cos(theta),
            -23 + r * math.cos(phi),
            r * math.sin(phi) * math.sin(theta),
            (255, 215, 185), 2.2, 0, False, 0
        ])
    for _ in range(30):
        sleigh_particles.append([
            -76 + random.uniform(-2, 3),
            -20 + random.uniform(0, 8),
            random.uniform(-5, 5),
            (255, 255, 255), 2.3, 0, True, 0
        ])
    sleigh_particles.append([-87, -33, 0, (255, 255, 255), 3.2, 0, True, 0])

    # (B) 루돌프와 사슴 5마리 편대
    reindeer_configs = [
        (-25, -11, False, 0.0),
        (-25,  11, False, 1.5),
        (22,  -11, False, 3.0),
        (22,   11, False, 4.5),
        (68,    0, True,  0.8),   # 선두 빨간 코 루돌프
    ]

    for rx_base, rz_base, is_rudolph, phase_off in reindeer_configs:
        fur_color = (215, 145, 75) if is_rudolph else (185, 120, 60)
        for _ in range(55):
            lx = rx_base + random.uniform(-12, 12)
            ly = random.uniform(-4, 4)
            lz = rz_base + random.uniform(-4.5, 4.5)
            sleigh_particles.append([lx, ly, lz, fur_color, 2.0, phase_off, False, 1])
        for _ in range(25):
            t = random.uniform(0, 1)
            lx = rx_base + 11 + t * 6
            ly = -3 - t * 10
            lz = rz_base + random.uniform(-3, 3)
            sleigh_particles.append([lx, ly, lz, fur_color, 2.0, phase_off, False, 1])
        for side in (-2.5, 2.5):
            for h in range(4):
                sleigh_particles.append([rx_base + 14 - h * 0.6, -15 - h * 2.2, rz_base + side, (240, 215, 160), 1.8, phase_off, False, 1])
        for lx_off in (-8, 8):
            for lz_off in (-3, 3):
                for d in range(4):
                    sleigh_particles.append([rx_base + lx_off, 4 + d * 2.5, rz_base + lz_off, (150, 95, 45), 1.8, phase_off + lx_off, False, 2])
        if is_rudolph:
            sleigh_particles.append([rx_base + 20, -12, rz_base, (255, 30, 50), 4.2, 0, True, 1])

    # 고삐 연결선
    for i in range(45):
        t = i / 44
        lx = -75 + t * 155
        ly = -6 + math.sin(t * math.pi) * 4
        for side in (-8, 8):
            sleigh_particles.append([lx, ly, side * (1 - t * 0.7), (255, 220, 120), 1.3, 0, True, 0])

build_santa_sleigh_and_reindeer()

# 6. 산타가 떨어뜨리는 3D 선물 꾸러미 생성 함수
GIFT_PALETTES = [
    ((255, 55, 85),  (255, 225, 70)),   # 빨강 상자 + 금색 리본
    ((50, 160, 255), (255, 255, 255)),  # 파랑 상자 + 흰색 리본
    ((190, 75, 255), (255, 215, 0)),    # 보라 상자 + 금색 리본
    ((55, 225, 130), (255, 65, 95)),    # 초록 상자 + 빨강 리본
    ((255, 195, 45), (235, 45, 75)),    # 금색 상자 + 빨강 리본
]

def spawn_falling_gift(wx, wy, wz):
    box_color, ribbon_color = random.choice(GIFT_PALETTES)
    size = random.uniform(18, 25)
    half = size / 2
    local_pts = []

    # 미니 3D 큐브 선물 상자 파티클 생성
    for _ in range(95):
        face = random.randint(0, 5)
        u = random.uniform(-half, half)
        v = random.uniform(-half, half)
        if face == 0:    lx, ly, lz = u, -half, v
        elif face == 1:  lx, ly, lz = u, half, v
        elif face == 2:  lx, ly, lz = u, v, half
        elif face == 3:  lx, ly, lz = u, v, -half
        elif face == 4:  lx, ly, lz = half, v, u
        else:            lx, ly, lz = -half, v, u

        is_ribbon = False
        band = half * 0.28
        if face in (0, 1) and (abs(lx) < band or abs(lz) < band):
            is_ribbon = True
        elif face in (2, 3) and (abs(lx) < band or abs(ly) < band):
            is_ribbon = True
        elif face in (4, 5) and (abs(lz) < band or abs(ly) < band):
            is_ribbon = True

        c = ribbon_color if is_ribbon else box_color
        local_pts.append((lx, ly, lz, c, 2.2 if is_ribbon else 1.8, is_ribbon))

    # 위쪽 리본 매듭 장식
    for angle_deg in (0, 90):
        rad = math.radians(angle_deg)
        for s in (-4, 4):
            local_pts.append((s * math.cos(rad), -half - 3, s * math.sin(rad), ribbon_color, 2.5, True))

    falling_gifts.append({
        "x": wx,
        "y": wy,
        "z": wz,
        "vy": random.uniform(1.6, 2.3),
        "vx": random.uniform(-0.35, 0.35),
        "vz": random.uniform(-0.35, 0.35),
        "rot_y": random.uniform(0, math.pi * 2),
        "rot_x": random.uniform(0, math.pi * 2),
        "vrot_y": random.uniform(-0.04, 0.04),
        "vrot_x": random.uniform(-0.03, 0.03),
        "landed": False,
        "life": 420,  # 바닥에 착지 후 유지 프레임 수 (약 7초 후 자연스럽게 사라짐)
        "pts": local_pts,
        "half": half,
    })

# 7. 꼭대기 별 파티클 추가
star_particles = []
for _ in range(120):
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)
    r = random.uniform(0, 18)
    sx = r * math.sin(phi) * math.cos(theta)
    sy = -305 + r * math.cos(phi)
    sz = r * math.sin(phi) * math.sin(theta)
    star_particles.append([sx, sy, sz])

# 8. 3D 눈(Snow) 파티클 생성
snow_particles = []
num_snow = 250
for _ in range(num_snow):
    sx = random.uniform(-500, 500)
    sy = random.uniform(-500, 500)
    sz = random.uniform(-350, 450)
    speed = random.uniform(1.2, 3.0)
    sway_phase = random.uniform(0, math.pi * 2)
    size = random.uniform(1.8, 3.8)
    snow_particles.append([sx, sy, sz, speed, sway_phase, size])

rotation_angle = 0
sleigh_orbit_angle = 0
last_drop_ms = 0
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 잔상 효과를 위한 반투명 검은 배경 덮기
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.set_alpha(95)
    fade.fill((5, 5, 12))
    screen.blit(fade, (0, 0))

    rotation_angle += 0.022      # 트리 회전 속도
    sleigh_orbit_angle += 0.018  # 산타 썰매 공전 속도
    cos_a = math.cos(rotation_angle)
    sin_a = math.sin(rotation_angle)
    fov = 620
    now_ms = pygame.time.get_ticks()

    render_list = []

    # (A) 회전하는 트리 + 나무 몸통 투영
    for x, y, z, color, size, phase, is_glow in tree_particles:
        rx = x * cos_a - z * sin_a
        rz = x * sin_a + z * cos_a

        scale = fov / (fov + rz + 430)
        sx = int(WIDTH / 2 + rx * scale)
        sy = int(HEIGHT / 2 + y * scale)

        if is_glow:
            twinkle = 0.75 + 0.25 * math.sin(now_ms * 0.008 + phase)
            c = tuple(min(255, int(ch * twinkle)) for ch in color)
        else:
            c = color

        render_list.append((rz, sx, sy, c, size * scale, is_glow))

    # (B) 고정된 선물 상자 + 여러 눈사람 투영
    for x, y, z, color, size, phase, is_glow in (gift_particles + snowman_particles):
        scale = fov / (fov + z + 430)
        sx = int(WIDTH / 2 + x * scale)
        sy = int(HEIGHT / 2 + y * scale)

        if is_glow:
            twinkle = 0.8 + 0.2 * math.sin(now_ms * 0.008 + phase)
            c = tuple(min(255, int(ch * twinkle)) for ch in color)
        else:
            c = color

        render_list.append((z, sx, sy, c, size * scale, is_glow))

    # (C) 산타 썰매 & 루돌프 3D 타원 궤도 투영
    orbit_rx = 300
    orbit_rz = 235
    cx_sleigh = orbit_rx * math.cos(sleigh_orbit_angle)
    cz_sleigh = orbit_rz * math.sin(sleigh_orbit_angle)
    cy_sleigh = -145 + math.sin(sleigh_orbit_angle * 2) * 28

    dx_dir = -orbit_rx * math.sin(sleigh_orbit_angle)
    dz_dir = orbit_rz * math.cos(sleigh_orbit_angle)
    heading = math.atan2(dz_dir, dx_dir)
    cos_h = math.cos(heading)
    sin_h = math.sin(heading)

    # 주기적으로(약 1.3초마다) 산타 썰매의 선물 보따리 위치에서 선물 꾸러미 투하
    if now_ms - last_drop_ms > 1300 and len(falling_gifts) < 10:
        last_drop_ms = now_ms
        sack_x = cx_sleigh + (-100 * cos_h)
        sack_z = cz_sleigh + (-100 * sin_h)
        sack_y = cy_sleigh + 8
        spawn_falling_gift(sack_x, sack_y, sack_z)

    for lx, ly, lz, color, size, phase, is_glow, anim_type in sleigh_particles:
        anim_x = lx
        anim_y = ly
        if anim_type == 1:
            anim_y += math.sin(now_ms * 0.012 + phase) * 2.5
        elif anim_type == 2:
            anim_x += math.sin(now_ms * 0.018 + phase) * 3.5
            anim_y += math.cos(now_ms * 0.018 + phase) * 1.5

        wx = cx_sleigh + (anim_x * cos_h - lz * sin_h)
        wz = cz_sleigh + (anim_x * sin_h + lz * cos_h)
        wy = cy_sleigh + anim_y

        scale = fov / (fov + wz + 430)
        sx = int(WIDTH / 2 + wx * scale)
        sy = int(HEIGHT / 2 + wy * scale)

        if is_glow:
            twinkle = 0.8 + 0.2 * math.sin(now_ms * 0.01 + phase)
            c = tuple(min(255, int(ch * twinkle)) for ch in color)
        else:
            c = color

        render_list.append((wz, sx, sy, c, size * scale, is_glow))

    # (D) 산타가 떨어뜨린 3D 선물 꾸러미 업데이트 및 투영
    active_gifts = []
    for g in falling_gifts:
        if not g["landed"]:
            g["x"] += g["vx"]
            g["y"] += g["vy"]
            g["z"] += g["vz"]
            g["vy"] += 0.035  # 중력 가속도
            g["rot_y"] += g["vrot_y"]
            g["rot_x"] += g["vrot_x"]

            # 바닥(y = 345)에 닿으면 착지
            if g["y"] + g["half"] >= 345:
                g["y"] = 345 - g["half"]
                g["landed"] = True
                g["rot_x"] = 0.0  # 바닥에 반듯하게 놓이도록 정렬
        else:
            g["life"] -= 1

        if g["life"] <= 0:
            continue
        active_gifts.append(g)

        fade_ratio = min(1.0, g["life"] / 60.0)
        cy_rot, sy_rot = math.cos(g["rot_y"]), math.sin(g["rot_y"])
        cx_rot, sx_rot = math.cos(g["rot_x"]), math.sin(g["rot_x"])

        for lx, ly, lz, color, size, is_glow in g["pts"]:
            # X축 회전 (낙하 중 빙글빙글 회전)
            y1 = ly * cx_rot - lz * sx_rot
            z1 = ly * sx_rot + lz * cx_rot
            # Y축 회전
            x2 = lx * cy_rot - z1 * sy_rot
            z2 = lx * sy_rot + z1 * cy_rot

            wx = g["x"] + x2
            wy = g["y"] + y1
            wz = g["z"] + z2

            scale = fov / (fov + wz + 430)
            sx = int(WIDTH / 2 + wx * scale)
            sy = int(HEIGHT / 2 + wy * scale)
            c = tuple(int(ch * fade_ratio) for ch in color)
            render_list.append((wz, sx, sy, c, size * scale, is_glow))

    falling_gifts = active_gifts

    # (E) 눈 파티클 이동 및 투영
    ticks = now_ms * 0.002
    for snow in snow_particles:
        snow[1] += snow[3]
        snow[0] += math.sin(ticks + snow[4]) * 0.4

        if snow[1] > 450:
            snow[1] = -500
            snow[0] = random.uniform(-500, 500)
            snow[2] = random.uniform(-350, 450)

        scale = fov / (fov + snow[2] + 430)
        sx = int(WIDTH / 2 + snow[0] * scale)
        sy = int(HEIGHT / 2 + snow[1] * scale)

        brightness = max(130, min(255, int(235 * scale)))
        snow_color = (brightness, brightness, min(255, brightness + 15))
        render_list.append((snow[2], sx, sy, snow_color, snow[5] * scale, False))

    # 깊이(Z축) 정렬
    render_list.sort(key=lambda item: item[0], reverse=True)

    for rz, sx, sy, c, s, is_glow in render_list:
        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            radius_px = max(1, int(s))
            if is_glow and radius_px >= 2:
                glow_color = (c[0] // 3, c[1] // 3, c[2] // 3)
                pygame.draw.circle(screen, glow_color, (sx, sy), radius_px * 2)
            pygame.draw.circle(screen, c, (sx, sy), radius_px)

    # 꼭대기 별 그리기
    for sx_3d, sy_3d, sz_3d in star_particles:
        rx = sx_3d * cos_a - sz_3d * sin_a
        rz = sx_3d * sin_a + sz_3d * cos_a
        scale = fov / (fov + rz + 430)
        px = int(WIDTH / 2 + rx * scale)
        py = int(HEIGHT / 2 + sy_3d * scale)
        pygame.draw.circle(screen, (255, 240, 150), (px, py), max(1, int(2.5 * scale)))

    # 9. 하단 네온 텍스트 그리기
    text_str = "Merry Christmas "
    pulse = 0.85 + 0.15 * math.sin(now_ms * 0.005)
    
    main_color = (int(255 * pulse), int(225 * pulse), int(110 * pulse))
    glow_color = (int(180 * pulse), int(110 * pulse), int(20 * pulse))

    glow_surf = font.render(text_str, True, glow_color)
    main_surf = font.render(text_str, True, main_color)

    text_rect = main_surf.get_rect(center=(WIDTH // 2, HEIGHT - 55))

    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
        screen.blit(glow_surf, text_rect.move(dx, dy))
    screen.blit(main_surf, text_rect)

    pygame.display.flip()

pygame.quit()
