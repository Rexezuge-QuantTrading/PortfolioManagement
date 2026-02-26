import { injectable } from 'tsyringe';
import { UserRepository } from '../repositories/UserRepository';

@injectable()
export class UserService {
  constructor(private userRepository: UserRepository) {}

  async getUser(id: string) {
    return this.userRepository.findById(id);
  }
}
