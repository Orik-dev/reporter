# """
# Сервис DeepSeek AI для генерации форматированных отчетов
# """
# import httpx
# from typing import List, Dict
# from loguru import logger
# from config.settings import settings


# class DeepSeekService:
#     """Сервис для взаимодействия с DeepSeek API"""
    
#     def __init__(self):
#         self.api_key = settings.deepseek_api_key
#         self.api_url = settings.deepseek_api_url
#         self.timeout = 60.0  # Таймаут запроса в секундах
    
#     async def generate_weekly_report(
#         self,
#         reports_data: List[Dict],
#         language: str = "ru"
#     ) -> str:
#         """
#         Сгенерировать форматированный недельный отчет с помощью AI
        
#         Args:
#             reports_data: Список ежедневных отчетов с информацией о пользователях
#             language: Язык отчета (ru или az)
        
#         Returns:
#             Отформатированный текст отчета
#         """
#         try:
#             # Подготавливаем промпт для AI
#             prompt = self._create_weekly_report_prompt(reports_data, language)
            
#             # Вызываем DeepSeek API
#             response_text = await self._call_deepseek_api(prompt)
            
#             return response_text
        
#         except Exception as e:
#             logger.error(f"Ошибка генерации недельного отчета через DeepSeek: {e}")
#             # Возвращаем простой отчет если AI не работает
#             return self._generate_fallback_report(reports_data, language)
    
#     def _create_weekly_report_prompt(
#         self,
#         reports_data: List[Dict],
#         language: str
#     ) -> str:
#         """Создать промпт для AI на основе данных отчетов"""
        
#         # Подготавливаем текст отчетов
#         reports_text = ""
#         for report in reports_data:
#             date_str = report['date'].strftime("%Y-%m-%d")
#             user_name = f"{report['first_name']} {report['last_name']}"
            
#             reports_text += f"\n{date_str} - {user_name}:\n"
#             if report['has_tasks']:
#                 reports_text += f"{report['report_text']}\n"
#             else:
#                 no_tasks_text = "Задач не было" if language == "ru" else "Tapşırıq olmayıb"
#                 reports_text += f"{no_tasks_text}\n"
        
#         # Создаем промпт в зависимости от языка
#         if language == "ru":
#             prompt = f"""Ты - профессиональный аналитик. Создай детальный и структурированный отчет о работе команды за неделю на основе ежедневных отчетов сотрудников.

# Исходные данные:
# {reports_text}

# Требования к отчету:
# 1. Структурируй информацию по дням недели
# 2. Выдели ключевые достижения команды
# 3. Сгруппируй задачи по категориям (если возможно)
# 4. Укажи общую статистику (количество выполненных задач, активность сотрудников)
# 5. Используй профессиональный стиль изложения
# 6. Отчет должен быть на русском языке
# 7. Используй emoji для лучшей читаемости

# Формат отчета должен быть удобен для чтения руководством."""
#         else:
#             prompt = f"""Sən peşəkar analitiksan. İşçilərin gündəlik hesabatları əsasında həftəlik komanda işi haqqında ətraflı və strukturlaşdırılmış hesabat yarat.

# İlkin məlumatlar:
# {reports_text}

# Hesabat tələbləri:
# 1. Məlumatı həftənin günlərinə görə strukturlaşdır
# 2. Komandanın əsas nailiyyətlərini vurğula
# 3. Tapşırıqları kateqoriyalara görə qruplaşdır (mümkünsə)
# 4. Ümumi statistika göstər (yerinə yetirilmiş tapşırıqların sayı, işçilərin aktivliyi)
# 5. Peşəkar üslubda təqdim et
# 6. Hesabat Azərbaycan dilində olmalıdır
# 7. Daha yaxşı oxunaqlılıq üçün emoji istifadə et

# Hesabat formatı rəhbərlik tərəfindən oxumaq üçün rahat olmalıdır."""
        
#         return prompt
    
#     async def _call_deepseek_api(self, prompt: str) -> str:
#         """Вызвать DeepSeek API"""
#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json"
#         }
        
#         data = {
#             "model": "deepseek-chat",
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             "temperature": 0.7,  # Креативность ответа
#             "max_tokens": 4000  # Максимальная длина ответа
#         }
        
#         async with httpx.AsyncClient(timeout=self.timeout) as client:
#             try:
#                 response = await client.post(
#                     self.api_url,
#                     headers=headers,
#                     json=data
#                 )
#                 response.raise_for_status()
                
#                 result = response.json()
#                 return result['choices'][0]['message']['content']
            
#             except httpx.HTTPError as e:
#                 logger.error(f"HTTP ошибка при вызове DeepSeek API: {e}")
#                 raise
#             except Exception as e:
#                 logger.error(f"Ошибка вызова DeepSeek API: {e}")
#                 raise
    
#     def _generate_fallback_report(
#         self,
#         reports_data: List[Dict],
#         language: str
#     ) -> str:
#         """Сгенерировать простой отчет если AI не работает"""
        
#         if language == "ru":
#             report = "📊 ЕЖЕНЕДЕЛЬНЫЙ ОТЧЕТ\n\n"
#             report += f"Период: неделя с {reports_data[0]['date'].strftime('%d.%m.%Y')} "
#             report += f"по {reports_data[-1]['date'].strftime('%d.%m.%Y')}\n\n"
            
#             # Группируем по датам
#             from collections import defaultdict
#             by_date = defaultdict(list)
#             for r in reports_data:
#                 by_date[r['date'].strftime('%d.%m.%Y')].append(r)
            
#             for date, day_reports in sorted(by_date.items()):
#                 report += f"📅 {date}:\n"
#                 for r in day_reports:
#                     user_name = f"{r['first_name']} {r['last_name']}"
#                     if r['has_tasks']:
#                         report += f"  • {user_name}: {r['report_text']}\n"
#                     else:
#                         report += f"  • {user_name}: Задач не было\n"
#                 report += "\n"
#         else:
#             report = "📊 HƏFTƏLİK HESABAT\n\n"
#             report += f"Dövr: {reports_data[0]['date'].strftime('%d.%m.%Y')} - "
#             report += f"{reports_data[-1]['date'].strftime('%d.%m.%Y')} həftəsi\n\n"
            
#             from collections import defaultdict
#             by_date = defaultdict(list)
#             for r in reports_data:
#                 by_date[r['date'].strftime('%d.%m.%Y')].append(r)
            
#             for date, day_reports in sorted(by_date.items()):
#                 report += f"📅 {date}:\n"
#                 for r in day_reports:
#                     user_name = f"{r['first_name']} {r['last_name']}"
#                     if r['has_tasks']:
#                         report += f"  • {user_name}: {r['report_text']}\n"
#                     else:
#                         report += f"  • {user_name}: Tapşırıq olmayıb\n"
#                 report += "\n"
        
#         return report


# # Глобальный экземпляр сервиса DeepSeek
# deepseek_service = DeepSeekService()

"""
Сервис DeepSeek AI - ФИНАЛЬНАЯ ВЕРСИЯ
"""
import httpx
from typing import List, Dict
from loguru import logger
from config.settings import settings


class DeepSeekService:
    """Сервис для взаимодействия с DeepSeek API"""
    
    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.api_url = settings.deepseek_api_url
        self.timeout = 60.0
    
    async def generate_weekly_report(
        self,
        reports_data: List[Dict],
        language: str = "ru"
    ) -> str:
        """Сгенерировать недельный отчет"""
        try:
            prompt = self._create_weekly_report_prompt(reports_data, language)
            response_text = await self._call_deepseek_api(prompt)
            return response_text
        
        except Exception as e:
            logger.error(f"Ошибка DeepSeek API: {e}")
            logger.warning("Использую fallback-генерацию")
            return self._generate_fallback_report(reports_data, language)
    
    def _create_weekly_report_prompt(
        self,
        reports_data: List[Dict],
        language: str
    ) -> str:
        """
        ✅ ОБНОВЛЕНО: Улучшенный промпт - четко, структурировано, без воды
        """
        
        reports_text = ""
        for report in reports_data:
            date_str = report['date'].strftime("%Y-%m-%d")
            user_name = f"{report['first_name']} {report['last_name']}"
            
            reports_text += f"\n{date_str} - {user_name}:\n"
            if report['has_tasks']:
                reports_text += f"{report['report_text']}\n"
            else:
                no_tasks_text = "Задач не было" if language == "ru" else "Tapşırıq olmayıb"
                reports_text += f"{no_tasks_text}\n"
        
        if language == "ru":
            prompt = f"""Ты - бизнес-аналитик. Создай КРАТКИЙ и СТРУКТУРИРОВАННЫЙ еженедельный отчет для руководства.

ИСХОДНЫЕ ДАННЫЕ:
{reports_text}

КРИТИЧЕСКИ ВАЖНО:
- НЕТ вводных фраз и воды
- НЕТ заключительных выводов
- ТОЛЬКО конкретные факты и цифры
- Максимальная информативность

СТРУКТУРА ОТЧЕТА:

**📊 СТАТИСТИКА НЕДЕЛИ**
- Количество сотрудников: X
- Отчетов подано: X
- Без задач: X

**📅 КЛЮЧЕВЫЕ ЗАДАЧИ ПО ДНЯМ**

*Понедельник (ДД.ММ):*
- Сотрудник 1: конкретная задача
- Сотрудник 2: конкретная задача

*Вторник (ДД.ММ):*
- ...

**🎯 ОСНОВНЫЕ НАПРАВЛЕНИЯ РАБОТЫ**
1. Направление 1 (X сотрудников)
   - Конкретные результаты
   
2. Направление 2 (X сотрудников)
   - Конкретные результаты

ТРЕБОВАНИЯ:
- Используй markdown (жирный, курсив, списки)
- Группируй похожие задачи
- Выделяй цифры и факты
- Максимум 300 слов
- НЕТ абстрактных фраз"""
        else:
            prompt = f"""Sən biznes-analitiksan. Rəhbərlik üçün QISA və STRUKTURLAŞDIRILMIŞ həftəlik hesabat yarat.

İLKİN MƏLUMAT:
{reports_text}

KRİTİK VACIB:
- Giriş cümlələri və "su" YOX
- Yekun nəticələr YOX
- YALNIZ konkret faktlar və rəqəmlər
- Maksimum informativlik

HESABAT STRUKTURU:

**📊 HƏFTƏ STATİSTİKASI**
- İşçi sayı: X
- Təqdim olunan hesabatlar: X
- Tapşırıqsız: X

**📅 GÜNLƏRƏ GÖRƏ ƏSAS TAPŞIRIQLAR**

*Bazar ertəsi (GG.AA):*
- İşçi 1: konkret tapşırıq
- İşçi 2: konkret tapşırıq

*Çərşənbə axşamı (GG.AA):*
- ...

**🎯 İŞİN ƏSAS İSTİQAMƏTLƏRİ**
1. İstiqamət 1 (X işçi)
   - Konkret nəticələr
   
2. İstiqamət 2 (X işçi)
   - Konkret nəticələr

TƏLƏBLƏR:
- Markdown istifadə et (qalın, kursiv, siyahı)
- Oxşar tapşırıqları qrupla
- Rəqəmləri və faktları vurğula
- Maksimum 300 söz
- Mücərrəd ifadələr YOX"""
        
        return prompt
    
    async def _call_deepseek_api(self, prompt: str) -> str:
        """Вызвать DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,  # ✅ СНИЖЕНО для большей точности
            "max_tokens": 2000  # ✅ СНИЖЕНО для краткости
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.api_url,
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
    
    def _generate_fallback_report(
        self,
        reports_data: List[Dict],
        language: str
    ) -> str:
        """Fallback отчет при недоступности API"""
        
        if language == "ru":
            report = "**📊 ЕЖЕНЕДЕЛЬНЫЙ ОТЧЕТ**\n\n"
            report += f"📅 Период: {reports_data[0]['date'].strftime('%d.%m.%Y')} - "
            report += f"{reports_data[-1]['date'].strftime('%d.%m.%Y')}\n"
            report += "⚠️ *Упрощенная версия*\n\n"
            
            from collections import defaultdict
            by_date = defaultdict(list)
            for r in reports_data:
                by_date[r['date'].strftime('%d.%m.%Y')].append(r)
            
            report += "**📅 ОТЧЕТЫ ПО ДНЯМ:**\n\n"
            for date, day_reports in sorted(by_date.items()):
                report += f"*{date}:*\n"
                for r in day_reports:
                    user_name = f"{r['first_name']} {r['last_name']}"
                    if r['has_tasks']:
                        report += f"• **{user_name}**: {r['report_text']}\n"
                    else:
                        report += f"• **{user_name}**: Задач не было\n"
                report += "\n"
            
            total = len(reports_data)
            with_tasks = sum(1 for r in reports_data if r['has_tasks'])
            
            report += "**📈 СТАТИСТИКА:**\n"
            report += f"• Всего отчетов: {total}\n"
            report += f"• С задачами: {with_tasks}\n"
            report += f"• Без задач: {total - with_tasks}\n"
            
        else:
            report = "**📊 HƏFTƏLİK HESABAT**\n\n"
            report += f"📅 Dövr: {reports_data[0]['date'].strftime('%d.%m.%Y')} - "
            report += f"{reports_data[-1]['date'].strftime('%d.%m.%Y')}\n"
            report += "⚠️ *Sadələşdirilmiş versiya*\n\n"
            
            from collections import defaultdict
            by_date = defaultdict(list)
            for r in reports_data:
                by_date[r['date'].strftime('%d.%m.%Y')].append(r)
            
            report += "**📅 GÜNLƏRƏ GÖRƏ HESABATLAR:**\n\n"
            for date, day_reports in sorted(by_date.items()):
                report += f"*{date}:*\n"
                for r in day_reports:
                    user_name = f"{r['first_name']} {r['last_name']}"
                    if r['has_tasks']:
                        report += f"• **{user_name}**: {r['report_text']}\n"
                    else:
                        report += f"• **{user_name}**: Tapşırıq olmayıb\n"
                report += "\n"
            
            total = len(reports_data)
            with_tasks = sum(1 for r in reports_data if r['has_tasks'])
            
            report += "**📈 STATİSTİKA:**\n"
            report += f"• Cəmi hesabat: {total}\n"
            report += f"• Tapşırıqlarla: {with_tasks}\n"
            report += f"• Tapşırıqsız: {total - with_tasks}\n"
        
        return report


deepseek_service = DeepSeekService()