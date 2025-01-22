import time
import threading

class BrewingProcess:
    def __init__(self, user_id):
        self._user_id = user_id
        self._bloom_time = 30           # 悶蒸時間, 秒
        self._total_pulsing = 3 * 60    # 總沖泡時間, 秒
        self.reset()

    def reset(self):
    #"""重置所有相關參數"""
        self._durations_pulse = []
        self._water_per_pulse = []
        self._total_ground = -1
        self._water_total = -1
        self._repeatCount = -1
        self._running = False

    def setData(self, water_total, total_ground, repeat_count):
    #"""設定沖泡參數"""
        self._water_total = float(water_total)
        self._total_ground = float(total_ground)
        self._repeatCount = int(repeat_count)

    def send_msg(self, message):
    #    """訊息處理，整合到 Line Bot 時替換為回覆機制"""
        print(message)

    def calculate_pulses(self):
    #"""計算每次沖泡的水量與時間"""
        remain_time = self._total_pulsing - self._bloom_time
        remain_water = self._water_total - self._total_ground * 2

    # 設定悶蒸時間和水量
        self._durations_pulse = [self._bloom_time]
        self._water_per_pulse = [self._total_ground * 2]

    # 每次注水時間和水量
        self.duration_per_pulse = remain_time // self._repeatCount
        self.water_per_pulse = remain_water // self._repeatCount

        for i in range(self._repeatCount):
            # 最後一次注水
            if i == self._repeatCount - 1:
                self._durations_pulse.append(remain_time)
                self._water_per_pulse.append(remain_water)
            else:
                self._durations_pulse.append(self.duration_per_pulse)
                self._water_per_pulse.append(self.water_per_pulse)

                # 更新剩餘時間和水量
                remain_time -= self.duration_per_pulse
                remain_water -= self.water_per_pulse
            
    def countdown_timer(self):
        """倒數計時器"""
        for idx, duration in enumerate(self._durations_pulse):
            water = self._water_per_pulse[idx]
            if idx == 0:
                msg = f"開始悶蒸{water}克"
            elif idx == len(self._durations_pulse)-1:
                msg = f"進行最後一次注水，{water}克，記得要在3分鐘以內流完唷！"
            else:
                msg = f"進行第{idx}次注水，{water}克。"
            
            self.send_msg(msg)

            while duration > 0:
                time.sleep(1)
                duration -= 1

        self.send_msg("沖泡完成")
        self.reset()

    def start(self):
        """啟動沖泡流程"""
        if self._running:
            self.send_msg("已經在執行沖煮計時！")
            return
        self._running = True
        self.calculate_pulses()
        threading.Thread(target=self.countdown_timer).start()


