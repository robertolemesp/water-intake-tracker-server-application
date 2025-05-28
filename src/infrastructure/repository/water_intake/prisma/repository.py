import logging
from datetime import date

from domain.shared.exceptions import DomainNotFoundError
from domain.water_intake.repository import WaterIntakeRepository

from infrastructure.database.connection import DatabaseConnection

logger = logging.getLogger("uvicorn.error")

class PrismaWaterIntakeRepository(WaterIntakeRepository):
  def __init__(self, db: DatabaseConnection):
    self.db = db
   # Obs.: Calcular as métricas via query escala melhor
   # (Menos consumo de CPU, RAM, Network; Mais velocidade - visto que os calculos PostgreSQL são feitos em C (que é bem mais rápido que python para operações numéricas); 
   # Atomicidade - o calculo e resultado acontecem em uma única e consistente transação no nível de banco de dados

  # Note: Calculate metrics via SQL scale better
  # (Less consumption of CPU, RAM, Network bandwidth. Faster execution, since PostgreSQL calculations are performed in C (which much faster than Python for numeric operations); 
  # Ensures atomicity — the calculation and the data retrieval happen in a single consistent transaction at the database level
  async def get_by_user_and_date(self, user_id: str, date: date, added_ml: int) -> dict | None:
    try:
      result = await self.db.query_raw("""
        SELECT 
          w.id,
          w."userId",
          w.date,
          w.ml,
          u."dailyGoalMl",
          GREATEST(u."dailyGoalMl" - w.ml - $3, 0) AS "remainingMlToGoal",
          ROUND(
            CASE 
              WHEN u."dailyGoalMl" = 0 THEN 0
              ELSE (($3 + w.ml)::float / u."dailyGoalMl") * 100
            END::numeric, 2
          ) AS "goalAverage",
          (w.ml >= u."dailyGoalMl") AS "isGoalAchieved"
        FROM "WaterIntake" w
        JOIN "User" u ON u.id = w."userId"
        WHERE w."userId" = $1 AND w.date = $2::date
        LIMIT 1;
      """, user_id, date.isoformat(), added_ml)

      if not result:
        user = await self.db.user.find_unique(where={'id': user_id})
        if not user:
          raise DomainNotFoundError('User', date.isoformat())
        
        return None
        
      row = result[0]

      return {
        'id': row['id'],
        'user_id': row['userId'],
        'date': row['date'],
        'ml': row['ml'],
        'daily_goal_ml': row['dailyGoalMl'],
        'remaining_ml_to_goal': row['remainingMlToGoal'],
        'goal_average': row['goalAverage'],
        'is_goal_achieved': row['isGoalAchieved']
      }
    except Exception as e:
      logger.exception('PrismaWaterIntakeRepository.get_by_user_and_date error occurred')
      raise e

  async def get_all_by_user_id(self, user_id: str) -> list[dict]:
    try: 
      result = await self.db.query_raw("""
        SELECT 
          w.id,
          w."userId",
          w.date,
          w.ml,
          u."dailyGoalMl",
          GREATEST(u."dailyGoalMl" - w.ml, 0) AS "remainingMlToGoal",
          ROUND(
            CASE 
              WHEN u."dailyGoalMl" = 0 THEN 0
              ELSE (w.ml::float / u."dailyGoalMl") * 100
            END::numeric, 2
          ) AS "goalAverage",
          (w.ml >= u."dailyGoalMl") AS "isGoalAchieved"
        FROM "WaterIntake" w
        JOIN "User" u ON u.id = w."userId"
        WHERE w."userId" = $1
        ORDER BY w.date ASC;
      """, user_id)

      if not result:
        user_exists = await self.db.user.find_unique(where={'id': user_id})
        if not user_exists:
          raise DomainNotFoundError('User', user_id)

      return [
        {
          'id': row['id'],
          'user_id': row['userId'],
          'date': row['date'],
          'ml': row['ml'],
          'daily_goal_ml': row['dailyGoalMl'],
          'remaining_ml_to_goal': row['remainingMlToGoal'],
          'goal_average': row['goalAverage'],
          'is_goal_achieved': row['isGoalAchieved']
        }
        for row in result
      ]
    except Exception as e:
      logger.exception('PrismaWaterIntakeRepository.get_all_by_user_id error occurred')
      raise e

  async def save(self, water_intake: dict) -> dict:
    try:
      payload = {
        'ml': water_intake['ml']
      }

      if water_intake['id']:
        updated_water_intake = await self.db.waterintake.update(
          where={'id': water_intake['id']},
          data=payload
        )

        return {
          'id': updated_water_intake.id,
          'user_id': updated_water_intake.userId,
          'date': updated_water_intake.date,
          'ml': updated_water_intake.ml
        }
      
      created_water_intake = await self.db.waterintake.create(
        data={
          'userId': water_intake['user_id'],
          'date':  f"{water_intake['date'].isoformat()}T00:00:00Z",
          **payload
        }
      )

      return {
        'id': created_water_intake.id,
        'user_id': created_water_intake.userId,
        'date': created_water_intake.date,
        'ml': created_water_intake.ml
      }
    
    except Exception as e:
      logger.exception('PrismaWaterIntakeRepository.save error occurred')
      raise e