    pressed_key = pygame.key.get_pressed()
            _platform.update(pressed_key)
            _ball.update()
            
            if score == BRICK_COLS * BRICKS_ROWS:
                wins = True
                pause = True