import { injectable } from 'tsyringe';

@injectable()
export class UserRepository {
  async findById(id: string) {
    return {
      id,
      name: 'John',
    };
  }
}
