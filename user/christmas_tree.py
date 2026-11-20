import math
import random
import pygame


# 초기화 및 화면 설정
pygame.init()
WIDTH, HEIGHT = 800, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Neon Particle Christmas Tree - Happy New Year")
clock = pygame.time.Clock()

# 폰트 설정 (HAPPY NEW YEAR! 텍스트용)
try:
    font = pygame.font.SysFont("arial", 46, bold=True)
except Exception:
    font = pygame.font.Font(None, 54)

tree_particles = []  # 회전하는 파티클 (나뭇잎 + 나무 몸통)
gift_particles = []  # 고정된 파티클 (선물 상자)

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

        # 상자의 초기 배치 각도만 적용
        rx = lx * cos_y - lz * sin_y + cx
        rz = lx * sin_y + lz * cos_y + cz
        ry = base_y + ly

        color = ribbon_color if is_ribbon else box_color
        gift_particles.append([rx, ry, rz, color, 2.3 if is_ribbon else 1.9, random.uniform(0, 6.28), is_ribbon])

# 선물 상자 4개 배치 (앞쪽/옆쪽에서 잘 보이도록 배치)
create_gift_box(-135, 95,  68, 55, 68, (230, 45, 75),  (255, 220, 60), 25)    # 왼쪽 앞 빨간 상자
create_gift_box(135,  85,  78, 46, 62, (45, 130, 245), (255, 255, 255), -20)  # 오른쪽 앞 파란 상자
create_gift_box(-85, -85,  58, 68, 58, (180, 65, 240), (255, 215, 0), 35)     # 왼쪽 뒤 보라 상자
create_gift_box(95,  -75,  62, 52, 62, (245, 195, 40), (235, 40, 60), -30)    # 오른쪽 뒤 금색 상자

# 4. 꼭대기 별 파티클 추가
star_particles = []
for _ in range(120):
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)
    r = random.uniform(0, 18)
    sx = r * math.sin(phi) * math.cos(theta)
    sy = -305 + r * math.cos(phi)
    sz = r * math.sin(phi) * math.sin(theta)
    star_particles.append([sx, sy, sz])

# 5. 3D 눈(Snow) 파티클 생성
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

    rotation_angle += 0.022  # 트리 회전 속도
    cos_a = math.cos(rotation_angle)
    sin_a = math.sin(rotation_angle)
    fov = 620

    render_list = []

    # (A) 회전하는 트리 + 나무 몸통 투영
    for x, y, z, color, size, phase, is_glow in tree_particles:
        rx = x * cos_a - z * sin_a
        rz = x * sin_a + z * cos_a

        scale = fov / (fov + rz + 430)
        sx = int(WIDTH / 2 + rx * scale)
        sy = int(HEIGHT / 2 + y * scale)

        if is_glow:
            twinkle = 0.75 + 0.25 * math.sin(pygame.time.get_ticks() * 0.008 + phase)
            c = tuple(min(255, int(ch * twinkle)) for ch in color)
        else:
            c = color

        render_list.append((rz, sx, sy, c, size * scale, is_glow))

    # (B) 고정된 선물 상자 투영 (회전 행렬 적용 안 함)
    for x, y, z, color, size, phase, is_glow in gift_particles:
        scale = fov / (fov + z + 430)
        sx = int(WIDTH / 2 + x * scale)
        sy = int(HEIGHT / 2 + y * scale)

        if is_glow:
            twinkle = 0.8 + 0.2 * math.sin(pygame.time.get_ticks() * 0.008 + phase)
            c = tuple(min(255, int(ch * twinkle)) for ch in color)
        else:
            c = color

        render_list.append((z, sx, sy, c, size * scale, is_glow))

    # (C) 눈 파티클 이동 및 투영
    ticks = pygame.time.get_ticks() * 0.002
    for snow in snow_particles:
        snow[1] += snow[3]  # y 낙하
        snow[0] += math.sin(ticks + snow[4]) * 0.4  # x 좌우 흔들림

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

    # 깊이(Z축) 정렬: 트리와 고정된 선물 상자, 눈이 입체적으로 겹치도록 정렬
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

    # 6. 하단 "HAPPY NEW YEAR!" 네온 텍스트 그리기
    text_str = "HAPPY NEW YEAR!"
    pulse = 0.85 + 0.15 * math.sin(pygame.time.get_ticks() * 0.005)
    
    # 네온 금빛 메인 색상 & 바깥쪽 후광 색상
    main_color = (int(255 * pulse), int(225 * pulse), int(110 * pulse))
    glow_color = (int(180 * pulse), int(110 * pulse), int(20 * pulse))

    glow_surf = font.render(text_str, True, glow_color)
    main_surf = font.render(text_str, True, main_color)

    text_rect = main_surf.get_rect(center=(WIDTH // 2, HEIGHT - 55))

    # 상하좌우로 약간씩 어긋나게 겹쳐 그려서 네온 발광 효과 연출
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
        screen.blit(glow_surf, text_rect.move(dx, dy))
    screen.blit(main_surf, text_rect)

    pygame.display.flip()

pygame.quit()
