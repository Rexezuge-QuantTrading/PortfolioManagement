import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand, PutCommand, UpdateCommand, DeleteCommand } from '@aws-sdk/lib-dynamodb';
import { Portfolio } from '@/dao/model/Portfolio';

const DEFAULT_LOCK_TIMEOUT_SECONDS = 30;

class DynamoDBPortfolioDAO {
  protected readonly tableName: string;
  protected readonly client: DynamoDBDocumentClient;

  constructor(tableName: string, _dynamoDBClient: DynamoDBClient) {
    const ddbClient = new DynamoDBClient({});

    this.client = DynamoDBDocumentClient.from(ddbClient, {
      marshallOptions: {
        removeUndefinedValues: true,
      },
    });

    this.tableName = tableName;
  }

  // =========================================================
  // Get Portfolio
  // =========================================================

  async getPortfolio(id: number, symbol: string): Promise<Portfolio | null> {
    const result = await this.client.send(
      new GetCommand({
        TableName: this.tableName,
        Key: {
          id,
          symbol,
        },
        ConsistentRead: true,
      }),
    );

    return (result.Item as Portfolio) ?? null;
  }

  // =========================================================
  // Create Portfolio (no lock)
  // =========================================================

  async createPortfolio(portfolio: Portfolio): Promise<void> {
    await this.client.send(
      new PutCommand({
        TableName: this.tableName,
        Item: portfolio,

        ConditionExpression: 'attribute_not_exists(id) AND attribute_not_exists(symbol)',
      }),
    );
  }

  // =========================================================
  // Acquire Lock (critical)
  // =========================================================

  async acquireLock(id: number, symbol: string, lockTimeoutSeconds: number = DEFAULT_LOCK_TIMEOUT_SECONDS): Promise<boolean> {
    const now = Math.floor(Date.now() / 1000);
    const newLockExpiry = now + lockTimeoutSeconds;

    try {
      await this.client.send(
        new UpdateCommand({
          TableName: this.tableName,

          Key: {
            id,
            symbol,
          },

          UpdateExpression: 'SET #lock = :newLock, updatedAt = :updatedAt',

          ConditionExpression: 'attribute_not_exists(#lock) OR #lock < :now',

          ExpressionAttributeNames: {
            '#lock': 'lock',
          },

          ExpressionAttributeValues: {
            ':newLock': newLockExpiry,
            ':now': now,
            ':updatedAt': now,
          },
        }),
      );

      return true;
    } catch (error: unknown) {
      if (error instanceof Error && error.name === 'ConditionalCheckFailedException') {
        return false;
      }

      throw error;
    }
  }

  // =========================================================
  // Release Lock
  // =========================================================

  async releaseLock(id: number, symbol: string): Promise<void> {
    const now = Math.floor(Date.now() / 1000);

    await this.client.send(
      new UpdateCommand({
        TableName: this.tableName,

        Key: {
          id,
          symbol,
        },

        UpdateExpression: 'SET #lock = :zero, updatedAt = :updatedAt',

        ExpressionAttributeNames: {
          '#lock': 'lock',
        },

        ExpressionAttributeValues: {
          ':zero': 0,
          ':updatedAt': now,
        },
      }),
    );
  }

  // =========================================================
  // Update Portfolio WITH LOCK REQUIRED
  // =========================================================

  async updatePortfolioWithLock(portfolio: Portfolio): Promise<void> {
    const now = Math.floor(Date.now() / 1000);

    await this.client.send(
      new UpdateCommand({
        TableName: this.tableName,

        Key: {
          id: portfolio.id,
          symbol: portfolio.symbol,
        },

        UpdateExpression: `
          SET quantity = :quantity,
              avgCostBasis = :avgCostBasis,
              updatedAt = :updatedAt
        `,

        ConditionExpression: '#lock > :now',

        ExpressionAttributeNames: {
          '#lock': 'lock',
        },

        ExpressionAttributeValues: {
          ':quantity': portfolio.quantity,

          ':avgCostBasis': portfolio.avgCostBasis,

          ':updatedAt': now,

          ':now': now,
        },
      }),
    );
  }

  // =========================================================
  // Delete Portfolio (requires lock)
  // =========================================================

  async deletePortfolio(id: number, symbol: string): Promise<void> {
    const now = Math.floor(Date.now() / 1000);

    await this.client.send(
      new DeleteCommand({
        TableName: this.tableName,

        Key: {
          id,
          symbol,
        },

        ConditionExpression: '#lock > :now',

        ExpressionAttributeNames: {
          '#lock': 'lock',
        },

        ExpressionAttributeValues: {
          ':now': now,
        },
      }),
    );
  }
}

export { DynamoDBPortfolioDAO };
