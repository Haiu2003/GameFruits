import random
import time

def game():
    total_score = 0
    round_number = 1
    game_duration = 60  # Độ dài trò chơi mỗi vòng là 60 giây
    total_rounds = 3  # Tổng số vòng chơi

    while round_number <= total_rounds:
        print("Vòng chơi", round_number)
        round_score = 0
        start_time = time.time()
        end_time = start_time + game_duration

        while time.time() < end_time:
            fruit = random.choice(["táo", "chuối", "cam"])
            print("Bắt", fruit)
            guess = input("Nhập 'b' để bắt hoặc 'q' để thoát: ").lower()

            if guess == "b":
                if fruit == "táo":
                    round_score += 1
                elif fruit == "chuối":
                    round_score += 2
                elif fruit == "cam":
                    round_score -= 1
                print("Điểm của bạn trong vòng này là:", round_score)
            elif guess == "q":
                print("Trò chơi kết thúc sớm!")
                return
            else:
                print("Nhập không hợp lệ!")

        print("Kết thúc vòng chơi", round_number)
        print("Điểm của bạn trong vòng này là:", round_score)
        total_score += round_score
        round_number += 1

    print("Kết thúc trò chơi!")
    print("Tổng điểm của bạn là:", total_score)

game()
